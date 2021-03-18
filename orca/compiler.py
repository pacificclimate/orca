"""The compiler module runs through all the steps to produce an ORCA output"""

from orca.db_handler import find_filepath, start_session
from orca.requester import build_opendap_url, file_from_opendap
from orca.utils import setup_logging


def orc(
    filepath,
    targets,
    thredds_base="https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets",
    outdir="/tmp/",
    outfile="",
    log_level="INFO",
):
    """OPeNDAP Request Complier

    Builds an OPeNDAP request that can be split into a series of requests and
    compiled back into a single output. This output is written to the `outpath`
    location and that same location is returned from this method.
    """
    logger = setup_logging(log_level)
    logger.info("Processing data file request")

    opendap_url = build_opendap_url(thredds_base, filepath, targets)
    logger.debug(f"Initial OPeNDAP URL: {opendap_url}")

    logger.info("Downloading data from OPeNDAP")
    outpath = file_from_opendap(opendap_url, outdir, outfile)
    logger.debug(f"Result avaialble at {outpath}")

    logger.info("Complete")
    return outpath
