import click
from orca import finder, request_opendap


@click.command()
@click.option(
    "-x",
    "--connection-string",
    help="Database connection string",
    default="postgresql://httpd_meta@db3.pcic.uvic.ca/pcic_meta",
)
@click.option("-u", "--unique-id", help="Unique_id to search for in DB")
@click.option("-v", "--variable", help="Variable of interest")
@click.option("-s", "--time_start", default=0, help="Start time")
@click.option("-e", "--time_end", default=55151, help="End time")
@click.option("-las", "--lat_start", default=0, help="Start longitude")
@click.option("-los", "--lon_start", default=0, help="Start longitude")
@click.option("-lae", "--lat_end", help="End latitude")
@click.option("-loe", "--lon_end", help="End longitude")
def process(
    connection_string,
    unique_id,
    variable,
    time_start,
    time_end,
    lat_end,
    lon_end,
    lat_start,
    lon_start,
):
    filepath = finder.find_filepath(connection_string, unique_id)
    print(filepath)
    url = request_opendap.build_url(
        filepath,
        variable,
        lat_end,
        lon_end,
        time_end,
        time_start,
        lat_start,
        lon_start,
    )
    print(url)
    r_status = request_opendap.request_opendap(url)
    print(r_status)


if __name__ == "__main__":
    process()
