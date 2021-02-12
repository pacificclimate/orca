import click
from orca import finder


@click.command()
@click.option(
    "-x",
    "--connection-string",
    help="Database connection string",
    default="postgres://ce_meta_ro@db3.pcic.uvic.ca/ce_meta_12f290b63791",
)
@click.option(
    "-f",
    "--filename",
    help="Filename to search for in DB"
)
def process(connection_string, filename):
    datafile = finder.find_filepath(connection_string, filename)
    print(datafile.filename)


if __name__ == "__main__":
    process()
