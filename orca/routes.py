"""Defines all routes available to Flask app"""

from flask import Blueprint, request, send_file
from tempfile import NamedTemporaryFile
from urllib.parse import unquote
from xarray import open_dataset
from orca.compiler import orc
from orca.requester import fill_target_bounds, to_file
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
    threshold = request.args.get("threshold", 5e8)
    outdir = request.args.get("outdir", os.getenv("TMPDIR", default="/tmp/"))
    outfile = request.args.get("outfile", "orca-output.nc")
    log_level = request.args.get("log_level", "INFO")

    # Flask will gobble the leading / and '+' signs for the storage path, add them back
    filepath = f"/{unquote(filepath)}"
    filepath = filepath.replace(" ", "+")
    # Add back '+' signs in output path if originally present
    outfile = outfile.replace(" ", "+")
    if targets:
        targets = unquote(targets)

    with NamedTemporaryFile(dir=outdir) as outpath:
        if not filepath.endswith("nc"):  # .dds, .dds, or .ascii request
            if targets:
                if (
                    "[]" in targets
                ):  # Unspecified bounds for downloading data in ascii format
                    nc_path = filepath[: filepath.rfind(".")]
                    dataset = open_dataset(f"{thredds_base}{nc_path}")
                    targets = fill_target_bounds(dataset, targets)
                url = f"{thredds_base}{filepath}?{targets}"
            else:
                url = f"{thredds_base}{filepath}"
            to_file(url, outdir="", outfile=outpath.name, nc=False)
        else:
            orc(
                filepath,
                targets,
                thredds_base,
                threshold,
                log_level,
                outdir="",
                outfile=outpath.name,
            )

        resp = send_file(
            outpath.name,
            as_attachment=True,
            download_name=outfile,
        )
    return resp
