"""Defines all routes available to Flask app"""

from flask import Blueprint, send_file
from orca.db_handler import find_filepath, start_session
from orca.requester import build_opendap_url, file_from_opendap
from orca.utils import setup_logging, get_filename_from_path


data = Blueprint("data", __name__, url_prefix="/data")


def orc(
    unique_id,
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

    logger.debug("Starting db session")
    sesh = start_session()
    filepath = find_filepath(sesh, unique_id)
    logger.debug(f"Got filepath: {filepath}")

    opendap_url = build_opendap_url(thredds_base, filepath, targets)
    logger.debug(f"Initial OPeNDAP URL: {opendap_url}")

    logger.info("Downloading data from OPeNDAP")
    outpath = file_from_opendap(opendap_url, outdir, outfile)
    logger.debug(f"Result avaialble at {outpath}")

    logger.info("Complete")
    return outpath


@data.route("/<string:unique_id>/<string:targets>", methods=["GET", "POST"])
def orc_route(unique_id, targets):
    """Wraps orc into a usable route with simplified inputs"""
    outpath = orc(unique_id, targets, log_level="DEBUG")

    return send_file(
        outpath,
        mimetype="application/x-netcdf",
        as_attachment=True,
        attachment_filename=get_filename_from_path(outpath),
    )
