import re
from xarray import open_dataset, load_dataset
from tempfile import NamedTemporaryFile

from .split import split_url


def request_opendap(url, req_limit=5e8):
    data = open_dataset(url)
    size = data.nbytes

    if size / 2 > req_limit:
        urls = split_url(url, size, req_limit)
    else:
        urls = [url]

    output = []
    for path in urls:
        tmp = NamedTemporaryFile(suffix=".nc", dir="/tmp")
        open_dataset(path).to_netcdf(tmp.name)
        output.append(tmp)

    return output


def build_url(thredds_base, filepath, variable, lat, lon):
    variable_form = re.compile(r"([a-z]*)(\[\d*(:\d*){1,2}\])")
    var_name, var_time = variable_form.findall(variable)[0][:2]

    return f"{thredds_base}{filepath}?{var_name}{var_time}{lat}{lon}"
