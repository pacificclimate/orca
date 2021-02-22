import pytest
from orca.bisect import bisect_request, split_url


@pytest.mark.parametrize(
    ("root"),
    [
        "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmax_day_BCCAQv2+ANUSPLIN300_bcc-csm1-1-m_historical+rcp26_r1i1p1_19500101-21001231.nc?<PARAMS>[0:1:509][0:1:1067]",
    ],
)
@pytest.mark.parametrize(
    ("var", "start", "step", "end"),
    [("tasmin", 0, "", 55113), ("tasmax", 0, ":1", 55114), ("pr", 78, ":5", 100)],
)
def test_bisect_request(root, var, start, step, end):
    url = root.replace("<PARAMS>", f"{var}[{start}{step}:{end}]")
    url1, url2 = bisect_request(url)
    mid = (start + end) // 2
    assert f"{var}[{start}{step}:{mid}]" in url1
    assert f"{var}[{mid+1}{step}:{end}]" in url2


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
    expected_chunks = -(-(size / 2) // 5e8)
    assert len(urls) == expected_chunks
