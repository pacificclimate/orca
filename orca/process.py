from .finder import find_filepath
from .request_opendap import build_url, request_opendap


def process_request(connection_string, unique_id, variable, lat, lon, out_file):
    """Uses orca modules to process output"""
    filepath = find_filepath(connection_string, unique_id)
    print(f"Got the filepath:{filepath}")

    url = build_url(filepath, variable, lat, lon)
    print(f"And now we got the url: {url}")

    request_opendap(url, out_file)
