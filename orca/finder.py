from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelmeta import DataFile


def find_filepath(connection_string, unique_id):
    """Given a unique_id, search pcic_meta for matching filepath"""
    Session = sessionmaker(create_engine(connection_string))
    sesh = Session()

    try:
        datafile = sesh.query(DataFile).filter(DataFile.unique_id == unique_id)
    except Exception as e:
        raise e

    if datafile.count() == 0:
        raise Exception(f"No match found with unique_id: {filename}")

    return datafile.first().filename
