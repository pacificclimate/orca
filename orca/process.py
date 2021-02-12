from .finder import find_filepath
from .request_opendap import build_url, request_opendap


def process_request(connection_string, unique_id, variable, lat, lon):
    """Uses orca modules to process output"""
    filepath = find_filepath(connection_string, unique_id)
    print(filepath)

    url = build_url(
        filepath,
        variable,
        lat,
        lon
    )
    print(url)
    r_status = request_opendap(url)
    print(r_status)
