from orca.db_handler import find_filepath, start_session
from orca.requester import build_opendap_url, file_from_opendap
from orca.utils import setup_logging


def orc(
    unique_id,
    targets,
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
    sesh = start_session()
    filepath = find_filepath(sesh, unique_id)
    logger.debug(f"Got filepath: {filepath}")

    opendap_url = build_opendap_url(thredds_base, filepath, targets)
    logger.debug(f"Initial OPeNDAP URL: {opendap_url}")

    logger.info("Downloading data from OPeNDAP")
    outpath = file_from_opendap(opendap_url, outdir)
    logger.debug(f"Result avaialble at {outpath}")

    logger.info("Complete")
    return outpath
