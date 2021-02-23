from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelmeta import DataFile


def find_filepath(sesh, unique_id):
    """Given a unique_id, search pcic_meta for matching filepath"""
    try:
        datafile = sesh.query(DataFile).filter(DataFile.unique_id == unique_id)
    except Exception as e:
        raise e

    if datafile.count() == 0:
        raise Exception(f"No match found with unique_id: {unique_id}")

    return datafile.first().filename


def start_session(connection_string):
    """Create session using connection string"""
    return sessionmaker(create_engine(connection_string))()
