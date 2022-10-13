"""Module responsible for handling requests to data servers"""

import logging
import requests
from xarray import open_mfdataset, open_dataset
import re
import os
from datetime import datetime


logger = logging.getLogger("scripts")


def file_from_opendap(url, outdir, outfile):
    """Write to file from OPeNDAP link"""
    urls = bisect_request(url)

    logger.debug(f"Downloading from {len(urls)} URL(s): {urls}")
    if len(urls) == 1:
        dataset = open_dataset(urls[0])
    else:
        dataset = open_mfdataset(urls, combine="nested", concat_dim="time")
    outpath = to_file(dataset, outdir, outfile)
    return outpath


def to_file(dataset, outdir, outfile="", nc=True):
    """Write data to generated filename"""
    if not outfile:
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        outfile = f"orca-output-{now}"

    outpath = outdir + outfile

    logger.debug("Begin file write")
    if nc:
        dataset.to_netcdf(outpath)
    else:
        f = open(outpath, "wb")
        f.write(requests.get(dataset).content)
        f.close()
    logger.debug("File write complete")

    return outpath


def build_opendap_url(thredds_base, filepath, targets):
    """Construct url for OPeNDAP. If target variables are not given, then all variables
    are added to the url to download the entire data file"""
    base_url = f"{thredds_base}{filepath}"
    dataset = open_dataset(base_url)
    if targets:
        targets = targets.replace(
            "[:]", "[]"
        )  # These are both treated as obtaining the full range of a dimension
        targets = fill_target_bounds(
            dataset, targets
        )  # Ensures that entire ranges of variables are obtained
    else:
        targets = build_all_targets(dataset)
    return f"{base_url}?{targets}"


def fill_target_bounds(dataset, targets):
    """Fill in bounds for variables in which they are unspecified"""
    dims = dataset.dims
    data_vars = dataset.data_vars

    target_list = targets.split(",")
    for (i, target) in enumerate(target_list):
        target_var = target.split("[", 1)[0]

        if target_var == target:  # No variable bounds are specified
            if target_var in dims:
                target += f"[0:{dims[target_var] - 1}]"
            else:
                sizes = "".join(
                    [f"[0:{end - 1}]" for end in data_vars[target_var].sizes.values()]
                )
                target += sizes
            target_list[i] = target

        elif ":]" in target:  # At least one variable has unspecified end bound
            if target_var in dims:
                target = target.replace(":]", f":{dims[target_var] - 1}]")
            else:
                target_bounds = "[" + target.split("[", 1)[1]
                target_bounds = target_bounds.replace("][", "],[")
                target_bound_list = target_bounds.split(",")

                # Add end bounds where needed
                for (j, end) in enumerate(data_vars[target_var].sizes.values()):
                    if ":]" in target_bound_list[j]:
                        target_bound_list[j] = target_bound_list[j].replace(
                            ":]", f":{end - 1}]"
                        )

                target_bounds = "".join(target_bound_list)
                target = target_var + target_bounds
            target_list[i] = target

        elif "[]" in target:  # At least one variable has unspecified bounds
            if target_var in dims:
                target = target.replace("[]", f"[0:{dims[target_var] - 1}]")
            else:
                target_bounds = "[" + target.split("[", 1)[1]
                target_bounds = target_bounds.replace("][", "],[")
                target_bound_list = target_bounds.split(",")

                # Replace bounds given by empty brackets with full ranges
                for (j, end) in enumerate(data_vars[target_var].sizes.values()):
                    if target_bound_list[j] == "[]":
                        target_bound_list[j] = f"[0:{end - 1}]"

                target_bounds = "".join(target_bound_list)
                target = target_var + target_bounds
            target_list[i] = target

    targets = ",".join(target_list)
    return targets


def build_all_targets(dataset):
    """Obtain all variable names and associated bounds so that all variables are
    retained when downloading an entire netCDF file. This also ensures the time bounds
    for the data variables and time coordinate are readily obtainable when bisecting the requests if needed."""
    dims = dataset.dims
    targets = ",".join(
        [f"{dim}[0:{end - 1}]" for (dim, end) in dims.items() if dim != "bnds"]
    )

    data_vars = dataset.data_vars
    data_var_list = []
    for var in data_vars.keys():
        sizes = "".join([f"[0:{end - 1}]" for end in data_vars[var].sizes.values()])
        data_var_list.append(f"{var}{sizes}")

    targets += ","
    targets += ",".join(data_var_list)
    return targets


def bisect_request(url, threshold=5e8):
    """Recursively bisect request until each piece is small enough for THREDDS

    OPeNDAP requests have a limit of 500MB, because of that we want to ensure
    that the request(s) we send are under that threshold. To do so we use the
    known initial request size to determine if we bisect the request. The base
    case is when a request is under the threshold. This method will construct
    a list of requests.

    NOTE: Server error reports dataset size = dataset.nbytes / 2. This method
    will maintain the size reported to ensure that the split is small enough
    to pass through the threshold.
    """
    dataset = open_dataset(url)
    bytes = dataset.nbytes

    if bytes < threshold:
        logger.debug(f"Request under threshold: {round(bytes * 10**-6)}/500 mb")
        return [url]

    else:
        logger.debug(
            f"Splitting, request over threshold: {round(bytes * 10**-6)}/500 mb"
        )

        # Bisect data variables
        front = url
        back = url
        bounds_format = r"(\[(\d+)(:\d+){0,1}:(\d+)\])"
        for data_var in dataset.data_vars:
            time_index = list(dataset[data_var].sizes).index("time")
            start_end_format = re.compile(
                rf"{data_var}{bounds_format}{{{time_index}}}{bounds_format}"
            )  # Last instance of bounds_format is the time component
            data_var_old = start_end_format.search(url)[
                0
            ]  # Format is data_var[...][time_bnds]
            time_bnds_old, start, stride, end = start_end_format.findall(data_var_old)[
                0
            ][-4:]

            pivot = int((int(start) + int(end)) / 2)
            time_bnds_front = f"[{start}{stride}:{pivot}]"
            time_bnds_back = f"[{pivot + 1}{stride}:{end}]"

            # Replace last occurence of old bounds with new bounds (avoid changing non-time bounds)
            time_pos = data_var_old.rfind(time_bnds_old)
            time_bnds_length = len(time_bnds_old)
            data_var_front = f"{data_var_old[:time_pos]}{time_bnds_front}{data_var_old[time_pos + time_bnds_length:]}"
            data_var_back = f"{data_var_old[:time_pos]}{time_bnds_back}{data_var_old[time_pos + time_bnds_length:]}"

            front = front.replace(data_var_old, data_var_front)
            back = back.replace(data_var_old, data_var_back)

        # Bisect time variable as well if it is requested
        time_format = re.compile(rf"time{bounds_format}")
        try:
            time_var = time_format.search(url)[0]
            start, stride, end = time_format.findall(time_var)[0][-3:]
            pivot = int((int(start) + int(end)) / 2)
            front = front.replace(time_var, f"time[{start}{stride}:{pivot}]")
            back = back.replace(time_var, f"time[{pivot + 1}{stride}:{end}]")
        except TypeError:  # time variable was not requested
            pass

        return bisect_request(front) + bisect_request(back)
