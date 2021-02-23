import pytest
from pathlib import Path
from xarray import open_dataset
from tempfile import NamedTemporaryFile
from orca.reconstruct import reconstruct_dataset


def reconstruct_dataset_test(data_files, url):
    with NamedTemporaryFile(suffix=".nc", dir="/tmp") as outfile:
        data_path = reconstruct_dataset(data_files, outfile.name)
        with open_dataset(data_path) as data, open_dataset(url) as expected_data:
            assert data.equals(expected_data)


@pytest.mark.online
@pytest.mark.parametrize(
    ("data_files", "source_url"),
    [
        (
            [
                f"{str(Path(__file__).parents[0])}/data/tasmin_sClimSD_anusplin_historical_19710101-20001231_time_0.nc",
                f"{str(Path(__file__).parents[0])}/data/tasmin_sClimSD_anusplin_historical_19710101-20001231_time_1.nc",
            ],
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/ANUSPLIN/climatologies/tasmin_sClimSD_anusplin_historical_19710101-20001231.nc?tasmin[0:1:1][0:1:0][0:1:0]",
        )
    ],
)
def test_reconstruct_dataset_online(data_files, source_url):
    reconstruct_dataset_test(data_files, source_url)


@pytest.mark.parametrize(
    ("data_files", "full_file"),
    [
        (
            [
                f"{str(Path(__file__).parents[0])}/data/tasmin_sClimSD_anusplin_historical_19710101-20001231_time_0.nc",
                f"{str(Path(__file__).parents[0])}/data/tasmin_sClimSD_anusplin_historical_19710101-20001231_time_1.nc",
            ],
            f"{str(Path(__file__).parents[0])}/data/tasmin_sClimSD_anusplin_historical_19710101-20001231_time_0to1.nc",
        )
    ],
)
def test_reconstruct_dataset_local(data_files, full_file):
    reconstruct_dataset_test(data_files, full_file)
