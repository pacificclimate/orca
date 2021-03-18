"""Module responsible for handling requests to data servers"""

import logging
from xarray import open_mfdataset, open_dataset
import re
from math import ceil
import os
from datetime import datetime


logger = logging.getLogger("scripts")


def file_from_opendap(url, outdir, outfile):
    """Write to file from OPeNDAP link"""
    urls = bisect_request(url)

    logger.debug(f"Downloading from {len(urls)} URL(s): {urls}")
    dataset = open_mfdataset(urls, combine="nested", concat_dim="time")
    outpath = to_file(dataset, outdir, outfile)

    return outpath


def to_file(dataset, outdir, outfile=""):
    """Write netcdf to generated filename"""
    if not outfile:
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        outfile = f"orca-output-{now}"

    outpath = outdir + outfile

    logger.debug("Begin file write")
    dataset.to_netcdf(outpath)
    logger.debug("File write complete")

    return outpath


def build_opendap_url(thredds_base, filepath, targets):
    """Construct url for OPeNDAP"""
    return f"{thredds_base}{filepath}?{targets}"


def bisect_request(url, threshold=5e8):
    """Based on the request range, split request into edible chunks for THREDDS

    OPeNDAP requests have a limit of 500MB, because of that we want to ensure
    that the request(s) we send are under that threshold. To do so we use the
    known initial request size and partition it into equal chunks (except for
    the leftover piece). If the request is under the threshold we can just
    return the url inside of a list.

    NOTE: Server error reports dataset size = dataset.nbytes / 2
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
