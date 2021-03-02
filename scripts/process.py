import click
from orca.main import orc


@click.command()
@click.option("--url", help="Data portal URL")
@click.option("--unique-id", help="Unique_id to search for in DB")
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
@click.option("-o", "--outfile", help="Output file path", default="outfile.nc")
@click.option("-l", "--log-level", help="Ouput file path", default="INFO")
def process(url, unique_id, connection_string, thredds_base, outfile, log_level):
    """CLI for orca"""
    orc(url, unique_id, connection_string, thredds_base, outfile, log_level)


if __name__ == "__main__":
    process()
