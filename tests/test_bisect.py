import pytest
from orca.bisect import bisect_request


@pytest.mark.parametrize(
    ("url"),
    [
        "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmax_day_BCCAQv2+ANUSPLIN300_bcc-csm1-1-m_historical+rcp26_r1i1p1_19500101-21001231.nc?lon[206:206],lat[91:91],time[0:55113],tasmax[0:1:0][0:1:0][0:1:0]",
        "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmax_day_BCCAQv2+ANUSPLIN300_bcc-csm1-1-m_historical+rcp26_r1i1p1_19500101-21001231.nc?lon[206:206],lat[91:91],time[0:1:55114],tasmax[0:1:0][0:1:0][0:1:0]",
    ],
)
def test_bisect_request(url):
    urls = bisect_request(url)
    print(urls)