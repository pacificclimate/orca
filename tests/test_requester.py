import pytest
import re
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


@pytest.mark.online
@pytest.mark.parametrize(
    "url",
    [
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?tasmin[0:1:1][0:1:1][0:1:1]"
        ),
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?tasmin[0:1:1000][0:1:200][0:1:200]"
        ),
    ],
)
def test_file_from_opendap(url):
    with NamedTemporaryFile(suffix=".nc", dir="/tmp") as temp:
        file_from_opendap(url, outdir="", outfile=temp.name)
        with open_dataset(url) as expected, open_dataset(temp.name) as data:
            assert expected.dims == data.dims


@pytest.mark.online
@pytest.mark.parametrize(
    ("thredds_base", "filepath"),
    [
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets",
            "/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmax_day_BCCAQv2+ANUSPLIN300_CSIRO-Mk3-6-0_historical+rcp85_r1i1p1_19500101-21001231.nc",
        ),
    ],
)
@pytest.mark.parametrize(
    ("targets"),
    [
        "tasmax[0:1:55114][91:91][206:1:206]",
        "tasmax[0:55114][91:91][206:1:206]",
    ],
)
def test_build_opendap_url(thredds_base, filepath, targets):
    url = build_opendap_url(thredds_base, filepath, targets)
    for expected in [thredds_base, filepath, targets]:
        assert expected in url


@pytest.mark.online
@pytest.mark.parametrize(
    ("url"),
    [
        "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc",
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
def test_fill_target_bounds(url, targets, expected):
    targets = fill_target_bounds(url, targets)
    target_list = targets.split(",")
    expected_list = expected.split(",")
    assert set(target_list) == set(expected_list)


@pytest.mark.online
@pytest.mark.parametrize(
    ("url", "expected"),
    [
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc",
            "lon[0:1067],lat[0:509],time[0:55114],tasmin[0:55114][0:509][0:1067]",
        ),
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/projects/comp_support/daccs/test-data/tasmin_mClim_BNU-ESM_historical_r1i1p1_19650101-19701230_test.nc",
            "lon[0:3],lon_bnds[0:3][0:1],lat[0:3],lat_bnds[0:3][0:1],time[0:11],climatology_bnds[0:11][0:1],tasmin[0:11][0:3][0:3]",
        ),
    ],
)
def test_build_all_targets(url, expected):
    targets = build_all_targets(url)
    target_list = targets.split(",")
    expected_list = expected.split(",")
    assert set(target_list) == set(expected_list)


@pytest.mark.online
@pytest.mark.parametrize(
    ("url", "expected"),
    [
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?tasmin[0:1:1000][0:1:91][0:1:206]",
            1,
        ),
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?tasmin[0:1:7500][0:1:91][0:1:206]",
            2,
        ),
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?tasmin[0:1:15000][0:1:91][0:1:206]",
            4,
        ),
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?tasmin[0:1:30000][0:1:91][0:1:206]",
            8,
        ),
    ],
)
def test_bisect_request(url, expected):
    urls = bisect_request(url)
    assert len(urls) == expected


@pytest.mark.online
@pytest.mark.parametrize(
    ("url", "expected"),
    [
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?time[0:1:7500],tasmin[0:1:7500][0:1:91][0:1:206]",
            [
                "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?time[0:1:3750],tasmin[0:1:3750][0:1:91][0:1:206]",
                "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?time[3751:1:7500],tasmin[3751:1:7500][0:1:91][0:1:206]",
            ],
        ),
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?time[0:1:15000],tasmin[0:1:15000][0:1:91][0:1:206]",
            [
                "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?time[0:1:3750],tasmin[0:1:3750][0:1:91][0:1:206]",
                "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?time[3751:1:7500],tasmin[3751:1:7500][0:1:91][0:1:206]",
                "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?time[7501:1:11250],tasmin[7501:1:11250][0:1:91][0:1:206]",
                "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?time[11251:1:15000],tasmin[11251:1:15000][0:1:91][0:1:206]",
            ],
        ),
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?time[0:1:30000],tasmin[0:1:30000][0:1:91][0:1:206]",
            [
                "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?time[0:1:3750],tasmin[0:1:3750][0:1:91][0:1:206]",
                "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?time[3751:1:7500],tasmin[3751:1:7500][0:1:91][0:1:206]",
                "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?time[7501:1:11250],tasmin[7501:1:11250][0:1:91][0:1:206]",
                "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?time[11251:1:15000],tasmin[11251:1:15000][0:1:91][0:1:206]",
                "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?time[15001:1:18750],tasmin[15001:1:18750][0:1:91][0:1:206]",
                "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?time[18751:1:22500],tasmin[18751:1:22500][0:1:91][0:1:206]",
                "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?time[22501:1:26250],tasmin[22501:1:26250][0:1:91][0:1:206]",
                "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc?time[26251:1:30000],tasmin[26251:1:30000][0:1:91][0:1:206]",
            ],
        ),
    ],
)
def test_bisect_request_with_time(url, expected):
    urls = bisect_request(url)
    assert urls == expected
