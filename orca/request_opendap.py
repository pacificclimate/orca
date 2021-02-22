import re
from xarray import open_dataset, load_dataset
from tempfile import NamedTemporaryFile

from .split import split_url


def request_opendap(url):
    data = open_dataset(url)
    size = data.nbytes
    dmb = size * (1e-6)

    if size / 2 > 5e8:
        urls = split_url(url, size)
    else:
        urls = [url]

    output = []
    for path in urls:
        tmp = NamedTemporaryFile(suffix=".nc", dir="/tmp")
        open_dataset(path).to_netcdf(tmp.name)
        output.append(tmp)

    # Move to reconstruction handler?
    (tmp.close for tmp in output)

    return output


def build_url(thredds_base, filepath, variable, lat, lon):
    variable_form = re.compile(r"([a-z]*)(\[\d*(:\d*){1,2}\])")
    var_name, var_time = variable_form.findall(variable)[0][:2]

    return f"{thredds_base}{filepath}?{var_name}{var_time}{lat}{lon}"
