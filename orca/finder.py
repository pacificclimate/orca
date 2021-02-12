from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelmeta import DataFile


def find_filepath(connection_string, filename):
    """Given a filename, search the ce_meta database for a match"""
    Session = sessionmaker(create_engine(connection_string))
    sesh = Session()

    try:
        datafile = sesh.query(DataFile).filter(DataFile.unique_id == filename)
    except Exception as e:
        raise e

    if datafile.count() == 0:
        raise Exception("No file found")

    return datafile.first()
