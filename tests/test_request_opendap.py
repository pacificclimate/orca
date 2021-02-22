import pytest
import re
from xarray import open_dataset
from orca.request_opendap import build_url, request_opendap
import numpy as np


@pytest.mark.parametrize(
    ("thredds_base", "filepath", "lat", "lon"),
    [
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets",
            "/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmax_day_BCCAQv2+ANUSPLIN300_CSIRO-Mk3-6-0_historical+rcp85_r1i1p1_19500101-21001231.nc",
            "[91:91]",
            "[206:1:206]",
        ),
    ],
)
@pytest.mark.parametrize(
    ("variable"),
    [
        "tasmax[0:1:55114]",
        "tasmax[0:55114]",
    ],
)
def test_build_url(thredds_base, filepath, variable, lat, lon):
    url = build_url(thredds_base, filepath, variable, lat, lon)
    assert url.startswith(f"{thredds_base}{filepath}")
    assert url.endswith(f"{variable}{lat}{lon}")


@pytest.mark.online
@pytest.mark.parametrize(
    ("url"),
    [
        "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmax_day_BCCAQv2+ANUSPLIN300_HadGEM2-CC_historical+rcp45_r1i1p1_19500101-21001231.nc?tasmax[0:1:0][0:1:509][0:1:1067]",
        "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?tasmin[500:1:1100][0:1:509][0:1:1067]",
    ],
)
def test_request_opendap(url):
    tmp_files = request_opendap(url)
    constraint_format = re.compile(r":(\d*)\]")
    time, lat, lon = constraint_format.findall(url)
    for tmp in tmp_files:
        with open_dataset(tmp.name) as d:
            assert d.dims["lat"] == int(lat) + 1
            assert d.dims["lon"] == int(lon) + 1
        tmp.close()
