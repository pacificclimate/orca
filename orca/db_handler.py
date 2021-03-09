"""Module responsible for handling databse related actions"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelmeta import DataFile
import os


def find_filepath(sesh, unique_id):
    """Given a unique_id, search pcic_meta for matching filepath"""
    datafile = sesh.query(DataFile).filter(DataFile.unique_id == unique_id)

    if datafile.count() == 0:
        raise Exception(f"No match found with unique_id: {unique_id}")

    return datafile.first().filename


def start_session():
    """Create session using the data source name provided by the envorinment"""
    dsn = os.environ.get("DSN")

    if not dsn:
        raise Exception("No DSN found, please set the DSN envorinment variable.")

    return sessionmaker(create_engine(dsn))()
