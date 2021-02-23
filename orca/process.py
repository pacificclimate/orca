from .finder import find_filepath, start_session
from .request_opendap import build_url, request_opendap
from .utils import setup_logging


def process_request(
    connection_string, unique_id, thredds_base, variable, lat, lon, log_level="INFO"
):
    """Uses orca modules to process output"""
    logger = setup_logging(log_level)

    logger.info(f"Getting the filepath")
    filepath = find_filepath(connection_string, unique_id)
    logger.debug(f"filepath: {filepath}")

    logger.info(f"Building initial url")
    url = build_url(thredds_base, filepath, variable, lat, lon)
    logger.debug(f"url: {url}")

    temp_files = request_opendap(url)

    return temp_files
