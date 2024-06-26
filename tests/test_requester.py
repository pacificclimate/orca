import pytest
import re
import os
from pkg_resources import resource_filename
from math import ceil
from tempfile import NamedTemporaryFile
from xarray import open_dataset

from orca.requester import (
    file_from_opendap,
    build_opendap_url,
    fill_target_bounds,
    build_all_targets,
    bisect_request,
)

tmpdir = os.getenv("TMPDIR", default="/tmp")
thredds_base = os.getenv(
    "THREDDS_BASE",
    default="https://marble-dev01.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets",
)


@pytest.mark.online
@pytest.mark.parametrize(
    ("filepath"),
    [
        "/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc",
    ],
)
@pytest.mark.parametrize(
    "targets",
    [
        "tasmin[0:1:1][0:1:1][0:1:1]",
        "tasmin[0:1:1000][0:1:200][0:1:200]",
    ],
)
def test_file_from_opendap(filepath, targets):
    url = f"{thredds_base}{filepath}?{targets}"
    with NamedTemporaryFile(suffix=".nc", dir=tmpdir) as outfile:
        file_from_opendap(url, threshold=5e8, outdir="", outfile=outfile.name)
        with open_dataset(outfile.name) as result, open_dataset(url) as expected:
            assert result.dims == expected.dims
            assert all(
                [
                    data_var1 == data_var2
                    for (data_var1, data_var2) in zip(
                        result.data_vars, expected.data_vars
                    )
                ]
            )


@pytest.mark.online
@pytest.mark.parametrize(
    ("filepath"),
    [
        "/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmax_day_BCCAQv2+ANUSPLIN300_CSIRO-Mk3-6-0_historical+rcp85_r1i1p1_19500101-21001231.nc",
    ],
)
@pytest.mark.parametrize(
    ("targets"),
    [
        "tasmax[0:1:55114][91:91][206:1:206]",
        "tasmax[0:55114][91:91][206:1:206]",
    ],
)
def test_build_opendap_url(filepath, targets):
    url = build_opendap_url(thredds_base, filepath, targets)
    for expected in [thredds_base, filepath, targets]:
        assert expected in url


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
            "lon,lat[],time[0:50]",
            "lon[0:1067],lat[0:509],time[0:50]",
        ),
        (
            "time,tasmin",
            "time[0:55114],tasmin[0:55114][0:509][0:1067]",
        ),
        (
            "tasmin[0:500][][]",
            "tasmin[0:500][0:509][0:1067]",
        ),
    ],
)
def test_fill_target_bounds_online(filepath, targets, expected):
    url = f"{thredds_base}{filepath}"
    dataset = open_dataset(url)
    targets = fill_target_bounds(dataset, targets)
    target_list = targets.split(",")
    expected_list = expected.split(",")
    assert set(target_list) == set(expected_list)


@pytest.mark.online
@pytest.mark.parametrize(
    ("filepath"),
    [
        resource_filename(
            __name__,
            "data/tasmin_mClim_BNU-ESM_historical_r1i1p1_19650101-19701230_test.nc",
        ),
    ],
)
@pytest.mark.parametrize(
    ("targets", "expected"),
    [
        (
            "lon,lat[],time[0:50]",
            "lon[0:3],lat[0:3],time[0:50]",
        ),
        (
            "time[0:2:],tasmin[0:2:][][]",
            "time[0:2:11],tasmin[0:2:11][0:3][0:3]",
        ),
        (
            "tasmin[0:5][0:][0:]",
            "tasmin[0:5][0:3][0:3]",
        ),
    ],
)
def test_fill_target_bounds_local(filepath, targets, expected):
    dataset = open_dataset(filepath)
    targets = fill_target_bounds(dataset, targets)
    target_list = targets.split(",")
    expected_list = expected.split(",")
    assert set(target_list) == set(expected_list)


@pytest.mark.online
@pytest.mark.parametrize(
    ("filepath", "expected"),
    [
        (
            "/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc",
            "lon[0:1067],lat[0:509],time[0:55114],tasmin[0:55114][0:509][0:1067]",
        ),
        (
            "/storage/data/projects/comp_support/daccs/test-data/tasmin_mClim_BNU-ESM_historical_r1i1p1_19650101-19701230_test.nc",
            "lon[0:3],lon_bnds[0:3][0:1],lat[0:3],lat_bnds[0:3][0:1],time[0:11],climatology_bnds[0:11][0:1],tasmin[0:11][0:3][0:3]",
        ),
    ],
)
def test_build_all_targets_online(filepath, expected):
    url = f"{thredds_base}{filepath}"
    dataset = open_dataset(url)
    targets = build_all_targets(dataset)
    target_list = targets.split(",")
    expected_list = expected.split(",")
    assert set(target_list) == set(expected_list)


@pytest.mark.parametrize(
    ("filepath", "expected"),
    [
        (
            resource_filename(__name__, "data/tiny_hydromodel_gcm_climos.nc"),
            "lon[0:1],lat[0:1],depth[0:2],time[0:16],climatology_bnds[0:16][0:1],"
            "RUNOFF[0:16][0:1][0:1],BASEFLOW[0:16][0:1][0:1],EVAP[0:16][0:1][0:1],"
            "GLAC_MBAL_BAND[0:16][0:2][0:1][0:1],GLAC_AREA_BAND[0:16][0:2][0:1][0:1],SWE_BAND[0:16][0:2][0:1][0:1]",
        ),
        (
            resource_filename(
                __name__,
                "data/tasmin_mClim_BNU-ESM_historical_r1i1p1_19650101-19701230_test.nc",
            ),
            "lon[0:3],lon_bnds[0:3][0:1],lat[0:3],lat_bnds[0:3][0:1],time[0:11],climatology_bnds[0:11][0:1],tasmin[0:11][0:3][0:3]",
        ),
    ],
)
def test_build_all_targets_local(filepath, expected):
    dataset = open_dataset(filepath)
    targets = build_all_targets(dataset)
    target_list = targets.split(",")
    expected_list = expected.split(",")
    assert set(target_list) == set(expected_list)


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
            "tasmin[0:1:1000][0:1:91][0:1:206]",
            1,
        ),
        (
            "tasmin[0:1:12000][0:1:91][0:1:206]",
            2,
        ),
        (
            "tasmin[0:1:24000][0:1:91][0:1:206]",
            4,
        ),
    ],
)
def test_bisect_request(filepath, targets, expected):
    url = f"{thredds_base}{filepath}?{targets}"
    input_dataset = open_dataset(url)
    threshold = 5e8
    nbytes = input_dataset.nbytes / 2
    data_vars = input_dataset.data_vars
    time_indices = []
    for data_var in data_vars:
        time_indices.append(list(input_dataset[data_var].sizes).index("time"))
    urls = bisect_request(url, threshold, nbytes, data_vars, time_indices)
    assert len(urls) == expected


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
            "time[0:1:6000],tasmin[0:1:6000][0:1:91][0:1:206]",
            [
                "time[0:1:6000],tasmin[0:1:6000][0:1:91][0:1:206]",
            ],
        ),
        (
            "time[0:1:12000],tasmin[0:1:12000][0:1:91][0:1:206]",
            [
                "time[0:1:6000],tasmin[0:1:6000][0:1:91][0:1:206]",
                "time[6001:1:12000],tasmin[6001:1:12000][0:1:91][0:1:206]",
            ],
        ),
        (
            "time[0:1:24000],tasmin[0:1:24000][0:1:91][0:1:206]",
            [
                "time[0:1:6000],tasmin[0:1:6000][0:1:91][0:1:206]",
                "time[6001:1:12000],tasmin[6001:1:12000][0:1:91][0:1:206]",
                "time[12001:1:18000],tasmin[12001:1:18000][0:1:91][0:1:206]",
                "time[18001:1:24000],tasmin[18001:1:24000][0:1:91][0:1:206]",
            ],
        ),
        (
            "time[0:1:48000],tasmin[0:1:48000][0:1:91][0:1:206]",
            [
                "time[0:1:6000],tasmin[0:1:6000][0:1:91][0:1:206]",
                "time[6001:1:12000],tasmin[6001:1:12000][0:1:91][0:1:206]",
                "time[12001:1:18000],tasmin[12001:1:18000][0:1:91][0:1:206]",
                "time[18001:1:24000],tasmin[18001:1:24000][0:1:91][0:1:206]",
                "time[24001:1:30000],tasmin[24001:1:30000][0:1:91][0:1:206]",
                "time[30001:1:36000],tasmin[30001:1:36000][0:1:91][0:1:206]",
                "time[36001:1:42000],tasmin[36001:1:42000][0:1:91][0:1:206]",
                "time[42001:1:48000],tasmin[42001:1:48000][0:1:91][0:1:206]",
            ],
        ),
    ],
)
def test_bisect_request_with_time(filepath, targets, expected):
    url = f"{thredds_base}{filepath}?{targets}"
    input_dataset = open_dataset(url)
    threshold = 5e8
    nbytes = input_dataset.nbytes / 2
    data_vars = input_dataset.data_vars
    time_indices = []
    for data_var in data_vars:
        time_indices.append(list(input_dataset[data_var].sizes).index("time"))
    urls = bisect_request(url, threshold, nbytes, data_vars, time_indices)
    expected_urls = [f"{thredds_base}{filepath}?{e}" for e in expected]
    assert urls == expected_urls
