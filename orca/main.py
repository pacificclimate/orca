from .db_handler import find_filepath, start_session
from .requester import build_opendap_url, file_from_opendap
from .utils import setup_logging


def orc(
    unique_id,
    targets,
    connection_string="postgresql://httpd_meta@db3.pcic.uvic.ca/pcic_meta",
    thredds_base="https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets",
    outdir="/tmp/",
    log_level="INFO",
):
    """OPeNDAP Request Complier

    Builds an OPeNDAP request that can be split into a series of requests and
    compiled back into a single output. This output is written to the `outpath`
    location and that same location is returned from this method.
    """
    logger = setup_logging(log_level)
    logger.info("Processing data file request")

    logger.debug("Starting db session")
    sesh = start_session(connection_string)
    filepath = find_filepath(sesh, unique_id)
    logger.debug(f"Got filepath: {filepath}")

    opendap_url = build_opendap_url(thredds_base, filepath, variable, lat, lon)
    logger.debug(f"Initial OPeNDAP URL: {opendap_url}")

    logger.info("Downloading data from OPeNDAP")
    outpath = file_from_opendap(opendap_url, outdir)
    logger.debug(f"Result avaialble at {outpath}")

    logger.info("Complete")
    return outpath
