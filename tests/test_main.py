import pytest
from xarray import open_dataset
from tempfile import NamedTemporaryFile

from orca import main, requester, db_handler


def expected_url(thredds_base, connection_string, unique_id, variable, lat, lon):
    """Helper for asserting url construction"""
    sesh = db_handler.start_session(connection_string)
    filepath = db_handler.find_filepath(sesh, unique_id)
    return requester.build_url(thredds_base, filepath, variable, lat, lon)


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
def test_main(thredds_base, connection_string, unique_id, variable, lat, lon):
    with NamedTemporaryFile(suffix=".nc", dir="/tmp") as outfile:
        output = main.orc(
            connection_string, unique_id, variable, lat, lon, thredds_base, outfile.name
        )

        url = expected_url(
            thredds_base, connection_string, unique_id, variable, lat, lon
        )

        with open_dataset(url) as expected, open_dataset(output) as data:
            assert expected.dims == data.dims

        outfile.close()
