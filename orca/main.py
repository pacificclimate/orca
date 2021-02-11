from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import click


@click.command()
@click.option(
    "-x",
    "--connection-string",
    help="Database connection string",
    default="postgres://ce_meta_ro@db3.pcic.uvic.ca/ce_meta_12f290b63791",
)
def process(connection_string):
    engine = create_engine(connection_string)
    Session = sessionmaker(engine)
    sesh = Session()


if __name__ == "__main__":
    process()
