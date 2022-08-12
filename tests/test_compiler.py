import pytest
import os
from xarray import open_dataset
from tempfile import NamedTemporaryFile

from orca import compiler

tmpdir = os.getenv("TMPDIR", default="/tmp")
thredds_base = (
    "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets"
)


@pytest.mark.slow
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
            "tasmin[0:0][0:91][0:206]",
        ),
        (
            "tasmin[0:7500][0:91][0:206]",
            "tasmin[0:7500][0:91][0:206]",
        ),
        (
            "tasmin[0:100][][]",
            "tasmin[0:100][0:509][0:1067]",
        ),
        (
            "lon,lat,time[0:100],tasmin[0:100][:][:]",
            "lon[0:1067],lat[0:509],time[0:100],tasmin[0:100][0:509][0:1067]",
        ),
    ],
)
def test_orc(filepath, targets, expected):
    expected_url = f"{thredds_base}{filepath}?{expected}"
    with NamedTemporaryFile(suffix=".nc", dir=tmpdir) as outfile:
        outpath = compiler.orc(filepath, targets, outdir="", outfile=outfile.name)

        with open_dataset(outpath) as result, open_dataset(expected_url) as expected:
            assert result.dims == expected.dims

        outfile.close()


@pytest.mark.online
@pytest.mark.parametrize(
    ("filepath"),
    [
        "/storage/data/projects/comp_support/daccs/test-data/tiny_hydromodel_gcm_climos.nc",
        "/storage/data/projects/comp_support/daccs/test-data/tasmin_mClim_BNU-ESM_historical_r1i1p1_19650101-19701230_test.nc",
    ],
)
def test_orc_no_targets(filepath):
    expected_url = f"{thredds_base}{filepath}"
    with NamedTemporaryFile(suffix=".nc", dir=tmpdir) as outfile:
        outpath = compiler.orc(filepath, outdir="", outfile=outfile.name)

        with open_dataset(outpath) as result, open_dataset(expected_url) as expected:
            assert result.dims == expected.dims

        outfile.close()
