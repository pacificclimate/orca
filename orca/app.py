from flask import Flask, send_file
from .main import orc
from .utils import get_filename_from_path


app = Flask(__name__)


@app.route("/orca/<string:url>/<string:unique_id>", methods=["GET", "POST"])
def orca(url, unique_id):
    outpath = orc(url, unique_id)
    name = get_filename_from_path(outpath)

    return send_file(
        outpath,
        mimetype="application/x-netcdf",
        as_attachment=True,
        attachment_filename=name,
    )
