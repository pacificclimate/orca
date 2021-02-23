import pytest
import re
from math import ceil
from orca.split import split_url


@pytest.mark.parametrize(
    ("url", "size"),
    [
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmax_day_BCCAQv2+ANUSPLIN300_HadGEM2-CC_historical+rcp45_r1i1p1_19500101-21001231.nc?tasmax[0:1:450][0:1:509][0:1:1067]",
            982602720,
        ),
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?tasmin[100:1:1500][0:1:509][0:1:1067]",
            3052386720,
        ),
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?tasmin[500:1:1100][0:1:509][0:1:1067]",
            1309410720,
        ),
    ],
)
def test_split_url(url, size):
    urls = split_url(url, size)

    expected_chunks = ceil((size / 2) / 5e8)
    start_end_format = re.compile(r"[a-z]+\[(\d*)(:\d*){0,1}:(\d*)\]")
    start, stride, end = start_end_format.findall(url)[0]

    assert len(urls) == expected_chunks
    assert start in urls[0]
    assert end in urls[-1]
