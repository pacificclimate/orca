import pytest
from orca.request_opendap import build_url


@pytest.mark.parametrize(
    ("thredds_base", "filepath", "lat", "lon"),
    [
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets",
            "/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmax_day_BCCAQv2+ANUSPLIN300_CSIRO-Mk3-6-0_historical+rcp85_r1i1p1_19500101-21001231.nc",
            "[91:91]",
            "[206:206]",
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
    assert url.startswith(
        "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets"
    )
    assert url.endswith("[0:1:0][0:1:0][0:1:0]")
    assert filepath in url
    assert f",lat{lat}" in url
    assert f"?lon{lon}" in url
