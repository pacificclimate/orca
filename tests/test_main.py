import pytest
from xarray import open_dataset
from tempfile import NamedTemporaryFile

from orca import main, requester, db_handler


@pytest.mark.online
@pytest.mark.parametrize(
    ("unique_id"),
    [
        "tasmax_day_BCCAQv2_CanESM2_historical-rcp85_r1i1p1_19500101-21001231_Canada",
    ],
)
@pytest.mark.parametrize(
    ("targets", "expected"),
    [
        (
            "tasmax[0:0][0:91][0:206]",
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmax_day_BCCAQv2+ANUSPLIN300_CanESM2_historical+rcp85_r1i1p1_19500101-21001231.nc?tasmax[0:1:0][0:1:91][0:1:206]",
        ),
        (
            "tasmax[0:15000][0:91][0:206]",
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmax_day_BCCAQv2+ANUSPLIN300_CanESM2_historical+rcp85_r1i1p1_19500101-21001231.nc?tasmax[0:1:15000][0:1:91][0:1:206]",
        ),
    ],
)
def test_main(unique_id, targets, expected):
    with NamedTemporaryFile(suffix=".nc", dir="/tmp") as outfile:
        outpath = main.orc(unique_id, targets, outdir="", outfile=outfile.name)

        with open_dataset(outpath) as result, open_dataset(expected) as expected:
            assert result.dims == expected.dims

        outfile.close()
