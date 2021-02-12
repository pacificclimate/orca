import requests
from orca import finder

def request_opendap(url):
    r = requests.get(data_url)
    if r.status_code==200:
        return "sucess"
    else:
        return "failed"


def build_url(
    storage_path,
    var,
    lat_end,
    lon_end,
    time_end=55151,
    time_start=0,
    lat_start=0,
    lon_start=0,
):
    thredds_base = (
        "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets"
    )
    data_url = f"{thredds_base}{storage_path}?{var}[{time_start}:{time_end}][{lon_start}:{lon_end}][{lat_start}:{lat_end}]&"

    return data_url
