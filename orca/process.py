from .finder import find_filepath, start_session
from .request_opendap import build_url, request_opendap
from .utils import setup_logging


def process_request(
    connection_string,
    unique_id,
    thredds_base,
    variable,
    lat,
    lon,
    outfile,
    log_level="INFO",
):
    """Uses orca modules to process output"""
    logger = setup_logging(log_level)

    logger.info("Getting the filepath")
    sesh = start_session(connection_string)
    filepath = find_filepath(sesh, unique_id)
    logger.debug(f"filepath: {filepath}")

    logger.info("Building initial url")
    url = build_url(thredds_base, filepath, variable, lat, lon)
    logger.debug(f"url: {url}")

    logger.info("Downloading data")
    out_file = request_opendap(url, outfile)

    logger.info("Download complete")
    return out_file
