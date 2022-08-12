"""Defines all routes available to Flask app"""

from flask import Blueprint, request, send_file
from urllib.parse import unquote
from orca.compiler import orc
from orca.requester import to_file
from orca.utils import get_filename_from_path
import os

data = Blueprint("data", __name__, url_prefix="/data")


@data.route("/", methods=["GET", "POST"])
def orc_route():
    """Wraps orc into a usable route with simplified inputs"""
    filepath = request.args.get("filepath")
    targets = request.args.get("targets", None)
    thredds_base = request.args.get(
        "thredds_base",
        "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets",
    )
    outdir = request.args.get("outdir", os.getenv("TMPDIR", default="/tmp/"))
    outfile = request.args.get("outfile", "")
    log_level = request.args.get("log_level", "INFO")

    # Flask will gobble the leading / and '+' signs for the storage path, add them back
    filepath = f"/{unquote(filepath)}"
    filepath = filepath.replace(" ", "+")
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
