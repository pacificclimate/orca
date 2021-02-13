import requests
import re
from netCDF4 import Dataset


def request_opendap(url):
    # note: interestingly enough we can't actually download the url we make but can access it using a dataset obj... hmmm
    try:
        ds = Dataset(url)
    except Exception as e:
        raise e

    print(ds)

def build_url(filepath, variable, lat, lon):
    thredds_base = (
        "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets"
    )
    variable_form = re.compile('([a-z]*)(\[\d*:\d*:\d*\])')
    (var_name, var_time), = variable_form.findall(variable)

    # Expected format
    # ?lon[0:1:1067],lat[0:1:509],time[0:1:55114],tasmax[0:1:0][0:1:0][0:1:0]
    # hard-coding some stuff for now
    # https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmax_day_BCCAQv2+ANUSPLIN300_CSIRO-Mk3-6-0_historical+rcp85_r1i1p1_19500101-21001231.nc?lon[0:1:2],lat[0:1:2],time[0:1:2],tasmax[0:1:0][0:1:0][0:1:0]
    # https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmax_day_BCCAQv2+ANUSPLIN300_CSIRO-Mk3-6-0_historical+rcp85_r1i1p1_19500101-21001231.nc?lon[0:1],lat[0:1],time[0:1],tasmax[0:1:0][0:1:0][0:1:0]
    return f"{thredds_base}{filepath}?lon{lon},lat{lat},time{var_time},{var_name}[0:1:0][0:1:0][0:1:0]"
