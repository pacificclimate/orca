import requests
import re


def request_opendap(url):
    r = requests.get(url)
    print(r.content)
    if r.status_code==200:
        return "sucess"
    else:
        return "failed"


def build_url(filepath, variable, lat, lon):
    thredds_base = (
        "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets"
    )
    variable_form = re.compile('([a-z]*)(\[\d*:\d*\])')
    var_name, var_time = variable_form.match(variable).group(0)
    print(var_name, var_time)
    import sys
    sys.exit(0)


    # Expected format
    # ?lon[0:1:1067],lat[0:1:509],time[0:1:55114],tasmax[0:1:0][0:1:0][0:1:0]
    # hard-coding some stuff for now
    data_url = f"{thredds_base}{storage_path}?lon{lon},lat{lat},time{var_time},{var_name}[0:1:0][0:1:0][0:1:0]"

    return data_url
