"""Defines all routes available to Flask app"""

from flask import Blueprint, send_file
from urllib.parse import unquote
from orca.compiler import orc
from orca.requester import to_file
from orca.utils import get_filename_from_path


data = Blueprint("data", __name__, url_prefix="/data")


@data.route("/<path:filepath>", methods=["GET", "POST"])
@data.route("/<path:filepath>:<string:targets>", methods=["GET", "POST"])
def orc_route(filepath, targets=None):
    """Wraps orc into a usable route with simplified inputs"""
    # Flask will gobble the leading / for the storage path, add it back
    filepath = f"/{unquote(filepath)}"
    if targets:
        targets = unquote(targets)

    if not filepath.endswith("nc"):  # .dds, .dds, or .ascii request
        if targets:
            url = f"{thredds_base}{filepath}?{targets}"
        else:
            url = f"{thredds_base}{filepath}"
        outpath = to_file(url, outdir, outfile, nc=False)
    else:
        outpath = orc(filepath, targets, thredds_base, outdir, outfile, log_level)

    return send_file(
        outpath,
        as_attachment=True,
        download_name=get_filename_from_path(outpath),
    )
