import pytest
from xarray import open_dataset
from tempfile import NamedTemporaryFile

from orca import process, request_opendap, finder, split


def expected_url(thredds_base, connection_string, unique_id, variable, lat, lon):
    sesh = finder.start_session(connection_string)
    filepath = finder.find_filepath(sesh, unique_id)
    return request_opendap.build_url(thredds_base, filepath, variable, lat, lon)


@pytest.mark.online
@pytest.mark.parametrize(
    ("thredds_base", "connection_string", "unique_id", "lat", "lon"),
    [
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets",
            "postgresql://httpd_meta@db3.pcic.uvic.ca/pcic_meta",
            "tasmax_day_BCCAQv2_bcc-csm1-1-m_historical-rcp26_r1i1p1_19500101-21001231_Canada",
            "[0:1:91]",
            "[0:1:206]",
        )
    ],
)
@pytest.mark.parametrize(
    ("variable"),
    [
        "tasmax[0:1:0]",
        "tasmax[0:1:15000]",
    ],
)
def test_process(thredds_base, connection_string, unique_id, variable, lat, lon):
    with NamedTemporaryFile(suffix=".nc", dir="/tmp") as outfile:
        output_path = process.process_request(
            connection_string,
            unique_id,
            thredds_base,
            variable,
            lat,
            lon,
            outfile.name
        )

        url =  expected_url(
            thredds_base, connection_string, unique_id, variable, lat, lon
        )

        with open_dataset(url) as expected, open_dataset(
            output_path
        ) as data:
            assert expected.dims == data.dims