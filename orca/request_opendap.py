import re
from xarray import open_dataset


def request_opendap(url, out_file):
    try:
        d = open_dataset(url)
        d.to_netcdf(out_file)
    except Exception as e:
        raise e

    return out_file


def build_url(thredds_base, filepath, variable, lat, lon):
    variable_form = re.compile(r"([a-z]*)(\[\d*(:\d*){1,2}\])")
    var_name, var_time = variable_form.findall(variable)[0][:2]

    # Expected format
    # ?lon[0:1:1067],lat[0:1:509],time[0:1:55114],tasmax[0:1:0][0:1:0][0:1:0]
    return f"{thredds_base}{filepath}?lon{lon},lat{lat},time{var_time},{var_name}[0:1:0][0:1:0][0:1:0]"