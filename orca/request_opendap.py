import re
from xarray import open_dataset, load_dataset
from tempfile import NamedTemporaryFile

from .split import split_url


def request_opendap(url, logger, req_limit=5e8):
    data = open_dataset(url)
    size = data.nbytes

    logger.info(f"Splitting url: {url}")
    urls = split_url(url, size, req_limit) if size / 2 > req_limit else [url]

    output = []
    logger.info(f"Downloading {len(urls)} files after split")
    for path in urls:
        tmp = NamedTemporaryFile(suffix=".nc", dir="/tmp")
        logger.info(
            f"Downloading dataset {urls.index(path)+1} of {len(urls)} to {tmp.name}"
        )
        open_dataset(path).to_netcdf(tmp.name)
        output.append(tmp)

    return output


def build_url(thredds_base, filepath, variable, lat, lon):
    return f"{thredds_base}{filepath}?{variable}{lat}{lon}"
