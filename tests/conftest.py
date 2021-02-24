import pytest
import testing.postgresql
import datetime
from pathlib import Path
from xarray import open_dataset
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tempfile import NamedTemporaryFile
from modelmeta import DataFile, create_test_database


def make_data_file(i, run=None, timeset=None):
    return DataFile(
        id=i,
        filename=f"data_file_{i}",
        first_1mib_md5sum="first_1mib_md5sum",
        unique_id=f"unique_id_{i}",
        x_dim_name="lon",
        y_dim_name="lat",
        t_dim_name="time",
        index_time=datetime.datetime.now(),
        run=run,
        timeset=timeset,
    )


@pytest.fixture(scope="function")
def postgis_session():
    """
    Yields a blank PostGIS session with no tables or data
    """
    with testing.postgresql.Postgresql() as pg:
        engine = create_engine(pg.url())
        engine.execute("create extension postgis")
        sesh = sessionmaker(bind=engine)()

        yield sesh

        sesh.rollback()
        sesh.close()


@pytest.fixture(scope="function")
def meta_session(postgis_session):
    """
    Yields a PostGIS enabled session with pcic_meta schema but no data
    """
    engine = postgis_session.get_bind()
    create_test_database(engine)
    yield postgis_session


@pytest.fixture(scope="function")
def test_session(meta_session):
    """
    Yields a PostGIS enabled session with pcic_meta schema and test data
    """
    data_files = [make_data_file(i) for i in range(3)]
    meta_session.add_all(data_files)
    meta_session.commit()

    yield meta_session


@pytest.fixture
def temp_files():
    file_paths = [
        f"{str(Path(__file__).parents[0])}/data/tasmin_sClimSD_anusplin_historical_19710101-20001231_time_0.nc",
        f"{str(Path(__file__).parents[0])}/data/tasmin_sClimSD_anusplin_historical_19710101-20001231_time_1.nc",
    ]

    temp_files = []
    for path in file_paths:
        tmp = NamedTemporaryFile(suffix=".nc", dir="/tmp")
        with open_dataset(path) as d:
            d.to_netcdf(tmp.name)

        temp_files.append(tmp)

    yield temp_files
