"""Module responsible for handling requests to data servers"""

import logging
import requests
from xarray import open_mfdataset, open_dataset
import re
from math import ceil
import os
from datetime import datetime


logger = logging.getLogger("scripts")


def file_from_opendap(url, outdir, outfile):
    """Write to file from OPeNDAP link"""
    file_extension = url.split(".")[-1].split("?")[0]
    if file_extension != "nc":
        outpath = to_file(url, outdir, outfile, nc=False)
    else:
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
    if filepath.endswith("nc"):
        if targets:
            targets = targets.replace(
                "[:]", "[]"
            )  # These are both treated as obtaining the full range of a dimension
            targets = fill_target_bounds(
                f"{thredds_base}{filepath}", targets
            )  # Ensures that entire ranges of variables are obtained
        else:
            targets = build_all_targets(f"{thredds_base}{filepath}")
        return f"{thredds_base}{filepath}?{targets}"

    else:  # .dds, .dds, or .ascii request
        if targets:
            return f"{thredds_base}{filepath}?{targets}"
        else:
            return f"{thredds_base}{filepath}"


def fill_target_bounds(url, targets):
    """Fill in bounds for variables in which they are unspecified"""
    dataset = open_dataset(url)
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


def build_all_targets(url):
    """Obtain all variable names and associated bounds so that all variables are
    retained when downloading an entire netCDF file. This also ensures the time bounds
    for the data variables and time coordinate are readily obtainable when bisecting the requests if needed."""
    dataset = open_dataset(url)
    dims = dataset.dims
    targets = ",".join([f"{dim}[0:{end - 1}]" for (dim, end) in dims.items()])

    # Remove "bnds" from targets if present
    bnds_format = re.compile(r"bnds\[(\d+)(:\d+){0,1}:(\d+)\]")
    try:
        bnds_var = bnds_format.search(targets)[0]
        targets = targets.replace(f",{bnds_var}", "")
    except TypeError:
        pass

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
    checkset = open_dataset(url)
    bytes = checkset.nbytes

    if bytes < threshold:
        logger.debug(f"Request under threshold: {round(bytes * 10**-6)}/500 mb")
        return [url]

    else:
        logger.debug(
            f"Splitting, request over threshold: {round(bytes * 10**-6)}/500 mb"
        )
        start_end_format = re.compile(r"(([a-z]+)\[(\d*)(:\d*){0,1}:(\d*)\])")
        var_time, var, start, stride, end = start_end_format.findall(url)[0]

        pivot = int((int(start) + int(end)) / 2)

        front = url.replace(var_time, f"{var}[{start}{stride}:{pivot}]")
        back = url.replace(var_time, f"{var}[{pivot + 1}{stride}:{end}]")

        return bisect_request(front) + bisect_request(back)
