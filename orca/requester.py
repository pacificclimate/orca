import logging
from xarray import open_mfdataset, open_dataset
import re
from math import ceil
import os
from datetime import datetime


logger = logging.getLogger("scripts")


def file_from_opendap(url, outdir):
    """Write to file from OPeNDAP link"""
    checkset = open_dataset(url)
    urls = split_url(url, checkset.nbytes)

    logger.debug(f"Downloading from {len(urls)} URL(s): {urls}")
    dataset = open_mfdataset(urls, combine="nested", concat_dim="time")
    outfile = to_file(dataset, outdir)

    return outfile


def to_file(dataset, outdir):
    """Write netcdf to generated filename"""
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


def split_url(url, size, threshold=5e8):
    """Based on the request range, split request into edible chunks for THREDDS

    OPeNDAP requests have a limit of 500MB, because of that we want to ensure
    that the request(s) we send are under that threshold. To do so we use the
    known initial request size and partition it into equal chunks (except for
    the leftover piece). If the request is under the threshold we can just
    return the url inside of a list.
    """
    bytes = size / 2

    if bytes > threshold:
        logger.debug(f"Splitting, request over threshold: {bytes * 10**-6}/500mb")
        start_end_format = re.compile(r"(([a-z]+)\[(\d*)(:\d*){0,1}:(\d*)\])")
        var_time, var, start, stride, end = start_end_format.findall(url)[0]
        start = int(start)
        end = int(end)

        # Server error reports dataset size = dataset.nbytes/2
        chunks = ceil(bytes / threshold)
        total = end - start
        step = int(total // chunks)

        chunk_end = start + step
        urls = []

        while chunk_end < end:
            urls.append(url.replace(var_time, f"{var}[{start}{stride}:{chunk_end}]"))
            start = chunk_end + 1
            chunk_end += step

        if start <= end:
            urls.append(url.replace(var_time, f"{var}[{start}{stride}:{end}]"))

        return urls

    else:
        logger.debug(f"Request under threshold: {bytes * 10**-6}/500mb")
        return [url]
