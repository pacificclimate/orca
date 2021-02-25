import click
from orca.main import orc


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
@click.option("-t", "--lat", help="Latitude slab as index (ex. [89:89])")
@click.option("-n", "--lon", help="Longitude slab as index (ex. [211:211])")
@click.option(
    "-b",
    "--thredds-base",
    help="Base path for all OPeNDAP links",
    default="https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets",
)
@click.option("-o", "--outfile", help="Output file path", default="outfile.nc")
@click.option("-l", "--log-level", help="Ouput file path", default="INFO")
def process(
    connection_string, unique_id, variable, lat, lon, thredds_base, outfile, log_level
):
    """CLI for orca"""
    print(connection_string)
    print(unique_id)
    print(variable)
    print(lat)
    print(lon)
    print(thredds_base)
    print(outfile)
    print(log_level)
    orc(
        connection_string,
        unique_id,
        variable,
        lat,
        lon,
        thredds_base,
        outfile,
        log_level,
    )


if __name__ == "__main__":
    process()
