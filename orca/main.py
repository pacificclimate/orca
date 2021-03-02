from .db_handler import find_filepath, start_session
from .requester import build_url, file_from_opendap, decompose_url
from .utils import setup_logging


def orc(
    url,
    unique_id,
    connection_string="postgresql://httpd_meta@db3.pcic.uvic.ca/pcic_meta",
    thredds_base="https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets",
    outfile="outfile.nc",
    log_level="INFO",
):
    """OPeNDAP Request Complier

    Builds an OPeNDAP request that can be split into a series of requests and
    compiled back into a single output.
    """
    logger = setup_logging(log_level)
    logger.info("Processing data file request")

    variable, lat, lon = decompose_url(url)

    logger.debug("Starting db session")
    sesh = start_session(connection_string)
    filepath = find_filepath(sesh, unique_id)
    logger.debug(f"Got filepath: {filepath}")

    url = build_url(thredds_base, filepath, variable, lat, lon)
    logger.debug(f"Initial url: {url}")

    logger.info("Downloading data file(s)")
    file_from_opendap(url, outfile)

    logger.info("Complete")
    return outfile
