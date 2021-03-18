import pytest
from xarray import open_dataset
from tempfile import NamedTemporaryFile

from orca import compiler


@pytest.mark.online
@pytest.mark.parametrize(
    ("filepath"),
    [
        "/storage/data/climate/downscale/CMIP5/BCSD/pr+tasmax+tasmin_day_BCSD+ANUSPLIN300+GFDL-ESM2G_historical+rcp26_r1i1p1_19500101-21001231.nc",
    ],
)
@pytest.mark.parametrize(
    ("targets", "expected"),
    [
        (
            "tasmax[0:0][0:91][0:206]",
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/CMIP5/BCSD/pr+tasmax+tasmin_day_BCSD+ANUSPLIN300+GFDL-ESM2G_historical+rcp26_r1i1p1_19500101-21001231.nc?tasmax[0:1:0][0:1:91][0:1:206]",
        ),
        (
            "tasmax[0:15000][0:91][0:206]",
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/CMIP5/BCSD/pr+tasmax+tasmin_day_BCSD+ANUSPLIN300+GFDL-ESM2G_historical+rcp26_r1i1p1_19500101-21001231.nc?tasmax[0:1:15000][0:1:91][0:1:206]",
        ),
    ],
)
def test_orc(filepath, targets, expected):
    with NamedTemporaryFile(suffix=".nc", dir="/tmp") as outfile:
        outpath = compiler.orc(filepath, targets, outdir="", outfile=outfile.name)

        with open_dataset(outpath) as result, open_dataset(expected) as expected:
            assert result.dims == expected.dims

        outfile.close()
