import pytest
from xarray import open_dataset
from tempfile import NamedTemporaryFile

from orca import process, request_opendap, finder, split


def expected_outputs(
    thredds_base, connection_string, unique_id, variable, lat, lon, req_limit=5e8
):
    filepath = finder.find_filepath(connection_string, unique_id)
    url = request_opendap.build_url(thredds_base, filepath, variable, lat, lon)

    with open_dataset(url) as data:
        split_urls = split.split_url(url, data.nbytes, req_limit)

    return url, split_urls


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
    data_files = process.process_request(
        connection_string,
        unique_id,
        thredds_base,
        variable,
        lat,
        lon,
    )

    url, split_urls = expected_outputs(
        thredds_base, connection_string, unique_id, variable, lat, lon
    )

    time_total = 0
    for i in range(len(data_files)):
        with open_dataset(split_urls[i]) as expected, open_dataset(
            data_files[i].name
        ) as output:
            assert expected.dims["time"] == output.dims["time"]
            time_total += output.dims["time"]

        data_files[i].close()

    with open_dataset(url) as data:
        assert time_total == data.dims["time"]
