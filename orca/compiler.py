"""The compiler module runs through all the steps to produce an ORCA output"""

from orca.requester import build_opendap_url, file_from_opendap
from orca.utils import setup_logging
import os


def orc(
    filepath,
    targets=None,
    thredds_base=os.getenv(
        "THREDDS_BASE",
        default="https://marble-dev01.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets",
    ),
    threshold=5e8,
    outdir=os.getenv("TMPDIR", default="/tmp/"),
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
    file_from_opendap(opendap_url, threshold, outdir, outfile)
    outpath = outdir + outfile
    logger.debug(f"Result available at {outpath}")

    logger.info("Complete")
