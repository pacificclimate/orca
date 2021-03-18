import pytest
import re
from math import ceil
from tempfile import NamedTemporaryFile
from xarray import open_dataset

from orca.requester import file_from_opendap, build_opendap_url, bisect_request


@pytest.mark.online
@pytest.mark.parametrize(
    "url",
    [
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?tasmin[0:1:1][0:1:1][0:1:1]"
        ),
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?tasmin[0:1:1000][0:1:200][0:1:200]"
        ),
    ],
)
def test_file_from_opendap(url):
    with NamedTemporaryFile(suffix=".nc", dir="/tmp") as temp:
        file_from_opendap(url, outdir="", outfile=temp.name)
        with open_dataset(url) as expected, open_dataset(temp.name) as data:
            assert expected.dims == data.dims


@pytest.mark.parametrize(
    ("thredds_base", "filepath"),
    [
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets",
            "/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmax_day_BCCAQv2+ANUSPLIN300_CSIRO-Mk3-6-0_historical+rcp85_r1i1p1_19500101-21001231.nc",
        ),
    ],
)
@pytest.mark.parametrize(
    ("targets"),
    [
        "tasmax[0:1:55114][91:91][206:1:206]",
        "tasmax[0:55114][91:91][206:1:206]",
    ],
)
def test_build_opendap_url(thredds_base, filepath, targets):
    url = build_opendap_url(thredds_base, filepath, targets)
    for expected in [thredds_base, filepath, targets]:
        assert expected in url


@pytest.mark.online
@pytest.mark.parametrize(
    ("url, expected"),
    [
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?tasmin[0:1:1000][0:1:91][0:1:206]",
            1,
        ),
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?tasmin[0:1:7500][0:1:91][0:1:206]",
            2,
        ),
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?tasmin[0:1:15000][0:1:91][0:1:206]",
            4,
        ),
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?tasmin[0:1:30000][0:1:91][0:1:206]",
            8,
        ),
    ],
)
def test_bisect_request(url, expected):
    urls = bisect_request(url)
    assert len(urls) == expected
