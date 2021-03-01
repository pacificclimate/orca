import click
from orca.requester import get_das
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
def das(connection_string, thredds_base, unique_id):
    """Collect DAS output given a unique_id"""
    sesh = start_session(connection_string)
    filepath = find_filepath(sesh, unique_id)

    das = get_das(thredds_base, filepath)
    print(das)


if __name__ == "__main__":
    das()
