import flask
from webapputils import Webapp
import requests

from .spec_parser import parse_oui_table

# Set up an app
app = Webapp(__name__, static_directory="static", google_tracking_code=None)

# OUI data remote
OUI_FILE_URL = "http://standards-oui.ieee.org/oui.txt"


@app.errorhandler(404)
def page_not_found(e):
    return flask.jsonify({"success": False, "message": "Not found"}), 404


@app.route("/lookup/<oui>")
def lookup(oui: str) -> flask.Response:

    # Grab a copy of the OUI database
    oui_db = requests.get(OUI_FILE_URL).text

    # Search for entry
    for vendor in parse_oui_table(oui_db):
        if vendor.oui == oui:
            return flask.jsonify({
                "success": "True",
                "vendor": vendor.__dict__()
            })

    # If the OUI id invalid
    return flask.jsonify({
        "success": False,
        "message": "OUI invalid or not assigned"
    }), 404


if __name__ == "__main__":
    app.run(debug=True)
