from flask import Flask, send_file
from .main import orc
from .utils import get_filename_from_path


app = Flask(__name__)


@app.route("/orca/<string:unique_id>/<string:targets>", methods=["GET", "POST"])
def orca(unique_id, targets):
    outpath = orc(unique_id, targets)

    return send_file(
        outpath,
        mimetype="application/x-netcdf",
        as_attachment=True,
        attachment_filename=get_filename_from_path(outpath),
    )
