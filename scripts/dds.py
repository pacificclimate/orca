import click
from orca.requester import get_dds
from orca.db_handler import find_filepath, start_session


@click.command()
@click.option(
    "-x",
    "--connection-string",
    help="Database connection string",
    default="postgresql://httpd_meta@db3.pcic.uvic.ca/pcic_meta",
)
@click.option(
    "-b",
    "--thredds-base",
    help="Base path for all OPeNDAP links",
    default="https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets",
)
@click.option("-u", "--unique-id", help="Unique_id to search for in DB")
@click.option("-v", "--variable", default="", help="Variable name")
def dds(connection_string, thredds_base, unique_id, variable):
    """Collect DDS output given a unique_id"""
    sesh = start_session(connection_string)
    filepath = find_filepath(sesh, unique_id)

    dds = get_dds(thredds_base, filepath, variable)
    print(dds)


if __name__ == "__main__":
    dds()
