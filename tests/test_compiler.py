import pytest
from xarray import open_dataset
from tempfile import NamedTemporaryFile

from orca import compiler


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
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?tasmin[0:0][0:91][0:206]",
        ),
        (
            "tasmin[0:7500][0:91][0:206]",
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?tasmin[0:7500][0:91][0:206]",
        ),
        (
            "tasmin[0:100][][]",
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?tasmin[0:100][0:509][0:1067]",
        ),
        (
            "lon,lat,time[0:100],tasmin[0:100][:][:]",
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?lon[0:1067],lat[0:509],time[0:100],tasmin[0:100][0:509][0:1067]",
        ),
    ],
)
def test_orc(filepath, targets, expected):
    with NamedTemporaryFile(suffix=".nc", dir="/tmp") as outfile:
        outpath = compiler.orc(filepath, targets, outdir="", outfile=outfile.name)

        with open_dataset(outpath) as result, open_dataset(expected) as expected:
            assert result.dims == expected.dims

        outfile.close()


@pytest.mark.online
@pytest.mark.parametrize(
    ("filepath", "expected"),
    [
        (
            "/storage/data/projects/comp_support/daccs/test-data/tiny_hydromodel_gcm_climos.nc",
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/projects/comp_support/daccs/test-data/tiny_hydromodel_gcm_climos.nc",
        ),
        (
            "/storage/data/projects/comp_support/daccs/test-data/tasmin_mClim_BNU-ESM_historical_r1i1p1_19650101-19701230_test.nc",
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/projects/comp_support/daccs/test-data/tasmin_mClim_BNU-ESM_historical_r1i1p1_19650101-19701230_test.nc",
        ),
    ],
)
def test_orc_no_targets(filepath, expected):
    with NamedTemporaryFile(suffix=".nc", dir="/tmp") as outfile:
        outpath = compiler.orc(filepath, outdir="", outfile=outfile.name)

        with open_dataset(outpath) as result, open_dataset(expected) as expected:
            assert result.dims == expected.dims

        outfile.close()


@pytest.mark.online
@pytest.mark.parametrize(
    ("filepath", "expected"),
    [
        (
            "/storage/data/projects/comp_support/daccs/test-data/tasmin_mClim_BNU-ESM_historical_r1i1p1_19650101-19701230_test.nc.dds",
            """Dataset {
    Float64 lon[lon = 4];
    Float64 lon_bnds[lon = 4][bnds = 2];
    Float64 lat[lat = 4];
    Float64 lat_bnds[lat = 4][bnds = 2];
    Float64 time[time = 12];
    Float64 climatology_bnds[time = 12][bnds = 2];
    Grid {
     ARRAY:
        Float32 tasmin[time = 12][lat = 4][lon = 4];
     MAPS:
        Float64 time[time = 12];
        Float64 lat[lat = 4];
        Float64 lon[lon = 4];
    } tasmin;
} datasets/storage/data/projects/comp_support/daccs/test-data/tasmin_mClim_BNU-ESM_historical_r1i1p1_19650101-19701230_test.nc;""",
        ),
        (
            "/storage/data/projects/comp_support/daccs/test-data/tasmin_mClim_BNU-ESM_historical_r1i1p1_19650101-19701230_test.nc.das",
            """Attributes {
    lon {
        String standard_name "longitude";
        String long_name "longitude";
        String units "degrees_east";
        String axis "X";
        String bounds "lon_bnds";
    }
    lon_bnds {
    }
    lat {
        String standard_name "latitude";
        String long_name "latitude";
        String units "degrees_north";
        String axis "Y";
        String bounds "lat_bnds";
    }
    lat_bnds {
    }
    time {
        String standard_name "time";
        String long_name "time";
        String climatology "climatology_bnds";
        String units "days since 1950-1-1 00:00:00";
        String calendar "365_day";
        String axis "T";
    }
    climatology_bnds {
    }
    tasmin {
        String standard_name "air_temperature";
        String long_name "Daily Maximum Near-Surface Air Temperature";
        String units "K";
        String grid_type "gaussian";
        Float32 _FillValue 1.0E20;
        Float32 missing_value 1.0E20;
        String cell_methods "time: maximum";
        String history "2012-03-12T06:02:42Z altered by CMOR: Treated scalar dimension: 'height'.";
        String associated_files "baseURL: http://cmip-pcmdi.llnl.gov/CMIP5/dataLocation gridspecFile: gridspec_atmos_fx_BNU-ESM_historical_r0i0p0.nc areacella: areacella_fx_BNU-ESM_historical_r0i0p0.nc";
    }""",
        ),
    ],
)
def test_orc_metadata_requests(filepath, expected):
    with NamedTemporaryFile(dir="/tmp") as outfile:
        outpath = compiler.orc(filepath, outdir="", outfile=outfile.name)
        if filepath.endswith(".das"):
            assert expected in open(outfile.name).read().rstrip("\n")
        else:
            assert open(outfile.name).read().rstrip("\n") == expected


@pytest.mark.online
@pytest.mark.parametrize(
    ("filepath", "targets", "expected"),
    [
        (
            "/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc.dds",
            "time",
            """Dataset {
    Float64 time[time = 55115];
} datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2%2bANUSPLIN300_inmcm4_historical%2brcp85_r1i1p1_19500101-21001231.nc;""",
        ),
        (
            "/storage/data/projects/comp_support/daccs/test-data/tasmin_mClim_BNU-ESM_historical_r1i1p1_19650101-19701230_test.nc.ascii",
            "lat,lon",
            """Dataset {
    Float64 lon[lon = 4];
    Float64 lat[lat = 4];
} datasets/storage/data/projects/comp_support/daccs/test-data/tasmin_mClim_BNU-ESM_historical_r1i1p1_19650101-19701230_test.nc;
---------------------------------------------
lon[4]
264.375, 267.1875, 270.0, 272.8125

lat[4]
65.57760620117188, 68.36775970458984, 71.15775299072266, 73.94751739501953""",
        ),
    ],
)
def test_orc_metadata_requests_with_targets(filepath, targets, expected):
    with NamedTemporaryFile(dir="/tmp") as outfile:
        outpath = compiler.orc(filepath, targets, outdir="", outfile=outfile.name)
        assert open(outfile.name).read().rstrip("\n") == expected
