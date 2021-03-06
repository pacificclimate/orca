import click
from orca.compiler import orc


@click.command()
@click.option("-p", "--filepath", help="Filepath to retrieve")
@click.option(
    "-t",
    "--targets",
    help="These are the data file targets in the form `variable[time_start:time_end][lat_start:lat_end][lon_start:lon_end]` (ex. tasmax[0:100][91:91][206:206])",
)
@click.option(
    "-b",
    "--thredds-base",
    help="Base path for all OPeNDAP links",
    default="https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets",
)
@click.option(
    "-o", "--outdir", help="Desired dir to store generated output", default="/tmp/"
)
@click.option("-f", "--outfile", help="Custom output filename", default="")
@click.option(
    "-l",
    "--log-level",
    help="Logging level",
    default="INFO",
    type=click.Choice(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
    ),
)
def process(filepath, targets, thredds_base, outdir, outfile, log_level):
    """CLI for orca"""
    orc(filepath, targets, thredds_base, outdir, outfile, log_level)


if __name__ == "__main__":
    process()
