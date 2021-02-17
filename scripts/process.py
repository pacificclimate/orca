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
    "-v", "--variable", help="Varible + time range string (ex. tasmax[0:55114])"
)
@click.option("-t", "--lat", help="Latitude slab as index (ex. [90:100])")
@click.option("-n", "--lon", help="Longitude slab as index (ex. [90:100])")
@click.option("-f", "--file", help="Output file path")
def process(connection_string, unique_id, variable, lat, lon, out_file):
    """CLI for orca"""
    process_request(connection_string, unique_id, variable, lat, lon, out_file)


if __name__ == "__main__":
    process()
