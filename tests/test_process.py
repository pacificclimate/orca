import pytest
from xarray import open_dataset
from tempfile import NamedTemporaryFile
from orca.process import process_request, build_url
from orca.finder import find_filepath


@pytest.mark.parametrize(
    ("filepath", "variable", "lat", "lon"),
    [
        (
            "/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmax_day_BCCAQv2+ANUSPLIN300_CSIRO-Mk3-6-0_historical+rcp85_r1i1p1_19500101-21001231.nc",
            "tasmax[0:1:55114]",
            "[91:91]",
            "[206:206]",
        ),
        (
            "/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmax_day_BCCAQv2+ANUSPLIN300_CSIRO-Mk3-6-0_historical+rcp85_r1i1p1_19500101-21001231.nc",
            "tasmax[0:55114]",
            "[91:91]",
            "[206:206]",
        ),
    ],
)
def test_build_url(filepath, variable, lat, lon):
    url = build_url(filepath, variable, lat, lon)
    assert url.startswith(
        "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets"
    )
    assert url.endswith("[0:1:0][0:1:0][0:1:0]")
    assert filepath in url
    assert f",lat{lat}" in url
    assert f"?lon{lon}" in url


@pytest.mark.online
@pytest.mark.parametrize(
    ("connection_string", "unique_id", "variable", "lat", "lon"),
    [
        (
            "postgresql://httpd_meta@db3.pcic.uvic.ca/pcic_meta",
            "tasmax_day_BCCAQv2_bcc-csm1-1-m_historical-rcp26_r1i1p1_19500101-21001231_Canada",
            "tasmax[0:1:55114]",
            "[91:91]",
            "[206:206]",
        )
    ],
)
def test_process(connection_string, unique_id, variable, lat, lon):
    with NamedTemporaryFile(
        suffix=".nc", prefix="output_", dir="/tmp", delete=True, mode="w+"
    ) as out_file:
        process_request(connection_string, unique_id, variable, lat, lon, out_file.name)
        filepath = find_filepath(connection_string, unique_id)
        url = build_url(filepath, variable, lat, lon)
        assert open_dataset(url, engine="netcdf4") == open_dataset(
            out_file.name, engine="netcdf4"
        )
