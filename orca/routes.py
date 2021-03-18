"""Defines all routes available to Flask app"""

from flask import Blueprint, send_file
from urllib.parse import unquote
from orca.compiler import orc
from orca.utils import get_filename_from_path


data = Blueprint("data", __name__, url_prefix="/data")


@data.route("/<path:filepath>:<string:targets>", methods=["GET", "POST"])
def orc_route(filepath, targets):
    """Wraps orc into a usable route with simplified inputs"""
    filepath = unquote(filepath)
    targets = unquote(targets)

    outpath = orc(filepath, targets, log_level="DEBUG")

    return send_file(
        outpath,
        mimetype="application/x-netcdf",
        as_attachment=True,
        attachment_filename=get_filename_from_path(outpath),
    )
