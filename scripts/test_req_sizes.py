import click
import time
import csv
from xarray import open_dataset
from tempfile import NamedTemporaryFile
from orca import main, requester, db_handler


def get_url(thredds_base, connection_string, unique_id, variable, lat, lon):
    """Helper for asserting url construction"""
    sesh = db_handler.start_session(connection_string)
    filepath = db_handler.find_filepath(sesh, unique_id)
    return requester.build_url(thredds_base, filepath, variable, lat, lon)


@click.command()
@click.option(
    "-x",
    "--connection-string",
    help="Database connection string",
    default="postgresql://httpd_meta@db3.pcic.uvic.ca/pcic_meta",
)
@click.option("-u", "--unique-id", help="Unique_id to search for in DB")
@click.option(
    "-b",
    "--thredds-base",
    help="Base path for all OPeNDAP links",
    default="https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets",
)
@click.option("-l", "--log-level", help="Ouput file path", default="INFO")
def test_req_sizes(connection_string, unique_id, thredds_base, log_level):
    lat = "[0:1:91]"
    lon = "[0:1:206]"

    with open("request_times.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Variable", "Size", "Time"])

        for i in range(1000, 55114, 7500):
            variable = f"tasmax[0:1:{i}]"

            url = get_url(
                thredds_base, connection_string, unique_id, variable, lat, lon
            )
            with open_dataset(url) as d:
                num_mb = (d.nbytes / 2) * 1e-6

            with NamedTemporaryFile(suffix=".nc", dir="/tmp") as outfile:
                start = time.time()
                main.orc(
                    connection_string,
                    unique_id,
                    variable,
                    lat,
                    lon,
                    thredds_base,
                    outfile.name,
                    log_level,
                )
                end = time.time()
            elapsed = end - start

            writer.writerow([variable])


if __name__ == "__main__":
    test_req_sizes()
