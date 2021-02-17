import click
from orca.process import process_request


@click.command()
@click.option(
    "-x",
    "--connection-string",
    help="Database connection string",
    default="postgresql://httpd_meta@db3.pcic.uvic.ca/pcic_meta",
)
@click.option("-u", "--unique-id", help="Unique_id to search for in DB")
@click.option(
    "-th",
    "--thredds-base",
    help="Base path for all OPeNDAP links",
    default="https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets",
)
@click.option(
    "-v", "--variable", help="Varible + time range string (ex. tasmax[0:55114])"
)
@click.option("-t", "--lat", help="Latitude slab as index (ex. [89:89])")
@click.option("-n", "--lon", help="Longitude slab as index (ex. [211:211])")
@click.option("-f", "--file", help="Output file path")
def process(connection_string, unique_id, thredds_base, variable, lat, lon, out_file):
    """CLI for orca"""
    process_request(
        connection_string, unique_id, thredds_base, variable, lat, lon, out_file
    )


if __name__ == "__main__":
    process()
