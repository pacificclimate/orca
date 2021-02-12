import click
from orca import finder


@click.command()
@click.option(
    "-x",
    "--connection-string",
    help="Database connection string",
    default="postgresql://httpd_meta@db3.pcic.uvic.ca/pcic_meta",
)
@click.option("-f", "--filename", help="Filename to search for in DB")
def process(connection_string, filename):
    datafile = finder.find_filepath(connection_string, filename)
    print(datafile.filename)


if __name__ == "__main__":
    process()
