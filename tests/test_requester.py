import pytest
import re
import os
from math import ceil
from tempfile import NamedTemporaryFile
from xarray import open_dataset

from orca.requester import (
    file_from_opendap,
    build_opendap_url,
    fill_target_bounds,
    build_all_targets,
    decrement_end_bounds,
    bisect_request,
)

tmpdir = os.getenv("TMPDIR", default="/tmp")
thredds_base = (
    "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets"
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
        "tasmin[0:1:2][0:1:2][0:1:2]",
        "tasmin[0:1:1001][0:1:201][0:1:201]",
    ],
)
def test_file_from_opendap(filepath, targets):
    url = f"{thredds_base}{filepath}?{targets}"
    with NamedTemporaryFile(suffix=".nc", dir=tmpdir) as outfile:
        file_from_opendap(url, outdir="", outfile=outfile.name)
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
    ("init_targets", "final_targets"),
    [
        (
            "tasmax[0:1:55115][91:92][206:1:207]",
            "tasmax[0:1:55114][91:91][206:1:206]",
        ),
        (
            "tasmax[0:55115][91:92][206:1:207]",
            "tasmax[0:55114][91:91][206:1:206]",
        ),
    ],
)
def test_build_opendap_url(filepath, init_targets, final_targets):
    url = build_opendap_url(thredds_base, filepath, init_targets)
    for expected in [thredds_base, filepath, final_targets]:
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
            "lon[0:1068],lat[0:510],time[0:50]",
        ),
        (
            "time,tasmin",
            "time[0:55115],tasmin[0:55115][0:510][0:1068]",
        ),
        (
            "tasmin[0:500][][]",
            "tasmin[0:500][0:510][0:1068]",
        ),
    ],
)
def test_fill_target_bounds(filepath, targets, expected):
    url = f"{thredds_base}{filepath}"
    targets = fill_target_bounds(url, targets)
    target_list = targets.split(",")
    expected_list = expected.split(",")
    assert set(target_list) == set(expected_list)


@pytest.mark.online
@pytest.mark.parametrize(
    ("filepath", "expected"),
    [
        (
            "/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc",
            "lon[0:1068],lat[0:510],time[0:55115],tasmin[0:55115][0:510][0:1068]",
        ),
        (
            "/storage/data/projects/comp_support/daccs/test-data/tasmin_mClim_BNU-ESM_historical_r1i1p1_19650101-19701230_test.nc",
            "lon[0:4],lon_bnds[0:4][0:2],lat[0:4],lat_bnds[0:4][0:2],time[0:12],climatology_bnds[0:12][0:2],tasmin[0:12][0:4][0:4]",
        ),
    ],
)
def test_build_all_targets(filepath, expected):
    url = f"{thredds_base}{filepath}"
    targets = build_all_targets(url)
    target_list = targets.split(",")
    expected_list = expected.split(",")
    assert set(target_list) == set(expected_list)


@pytest.mark.parametrize(
    ("targets", "expected"),
    [
        (
            "tasmin[0:1:1001][0:91][0:206]",
            "tasmin[0:1:1000][0:90][0:205]",
        ),
        (
            "time[0:1001],tasmin[0:1:1001][0:91][0:206]",
            "time[0:1000],tasmin[0:1:1000][0:90][0:205]",
        ),
    ],
)
def test_decrement_end_bounds(targets, expected):
    decremented = decrement_end_bounds(targets)
    assert decremented == expected


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
            "tasmin[0:1:7500][0:1:91][0:1:206]",
            2,
        ),
        (
            "tasmin[0:1:15000][0:1:91][0:1:206]",
            4,
        ),
        (
            "tasmin[0:1:30000][0:1:91][0:1:206]",
            8,
        ),
    ],
)
def test_bisect_request(filepath, targets, expected):
    url = f"{thredds_base}{filepath}?{targets}"
    urls = bisect_request(url)
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
            "time[0:1:7500],tasmin[0:1:7500][0:1:91][0:1:206]",
            [
                "time[0:1:3750],tasmin[0:1:3750][0:1:91][0:1:206]",
                "time[3751:1:7500],tasmin[3751:1:7500][0:1:91][0:1:206]",
            ],
        ),
        (
            "time[0:1:15000],tasmin[0:1:15000][0:1:91][0:1:206]",
            [
                "time[0:1:3750],tasmin[0:1:3750][0:1:91][0:1:206]",
                "time[3751:1:7500],tasmin[3751:1:7500][0:1:91][0:1:206]",
                "time[7501:1:11250],tasmin[7501:1:11250][0:1:91][0:1:206]",
                "time[11251:1:15000],tasmin[11251:1:15000][0:1:91][0:1:206]",
            ],
        ),
        (
            "time[0:1:30000],tasmin[0:1:30000][0:1:91][0:1:206]",
            [
                "time[0:1:3750],tasmin[0:1:3750][0:1:91][0:1:206]",
                "time[3751:1:7500],tasmin[3751:1:7500][0:1:91][0:1:206]",
                "time[7501:1:11250],tasmin[7501:1:11250][0:1:91][0:1:206]",
                "time[11251:1:15000],tasmin[11251:1:15000][0:1:91][0:1:206]",
                "time[15001:1:18750],tasmin[15001:1:18750][0:1:91][0:1:206]",
                "time[18751:1:22500],tasmin[18751:1:22500][0:1:91][0:1:206]",
                "time[22501:1:26250],tasmin[22501:1:26250][0:1:91][0:1:206]",
                "time[26251:1:30000],tasmin[26251:1:30000][0:1:91][0:1:206]",
            ],
        ),
    ],
)
def test_bisect_request_with_time(filepath, targets, expected):
    url = f"{thredds_base}{filepath}?{targets}"
    urls = bisect_request(url)
    expected_urls = [f"{thredds_base}{filepath}?{e}" for e in expected]
    assert urls == expected_urls
