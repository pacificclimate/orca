import pytest
import testing.postgresql
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelmeta import DataFile, create_test_database


def make_data_file(i, run=None, timeset=None):
    return DataFile(
        id=i,
        filename='data_file_{}'.format(i),
        first_1mib_md5sum='first_1mib_md5sum',
        unique_id='unique_id_{}'.format(i),
        x_dim_name='lon',
        y_dim_name='lat',
        t_dim_name='time',
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
