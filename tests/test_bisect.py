import pytest
from orca.bisect import bisect_request


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
