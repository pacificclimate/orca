import logging
from xarray import open_mfdataset, open_dataset
from tempfile import NamedTemporaryFile

from .split import split_url


def request_opendap(url):
    logger = logging.getLogger("scripts")

    data = open_dataset(url)
    size = data.nbytes

    logger.debug(f"Splitting url: {url}")
    urls = split_url(url, size)

    logger.debug(f"Downloading and merging {len(urls)} split files")
    tmp = NamedTemporaryFile(suffix=".nc", dir="/tmp")
    open_mfdataset(urls, combine="nested", concat_dim="time").to_netcdf(tmp.name)

    return tmp


def build_url(thredds_base, filepath, variable, lat, lon):
    return f"{thredds_base}{filepath}?{variable}{lat}{lon}"
