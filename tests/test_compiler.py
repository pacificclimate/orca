import pytest
from xarray import open_dataset
from tempfile import NamedTemporaryFile

from orca import compiler


@pytest.mark.online
@pytest.mark.parametrize(
    ("filepath"),
    [
        "/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc",
    ],
)
@pytest.mark.parametrize(
    ("targets", "expected"),
    [
        (
            "tasmin[0:0][0:91][0:206]",
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?tasmin[0:0][0:91][0:206]",
        ),
        (
            "tasmin[0:15000][0:91][0:206]",
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?tasmin[0:15000][0:91][0:206]",
        ),
    ],
)
def test_orc(filepath, targets, expected):
    with NamedTemporaryFile(suffix=".nc", dir="/tmp") as outfile:
        outpath = compiler.orc(filepath, targets, outdir="", outfile=outfile.name)

        with open_dataset(outpath) as result, open_dataset(expected) as expected:
            assert result.dims == expected.dims

        outfile.close()
