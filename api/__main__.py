import flask
from webapputils import Webapp
import requests
import os

from .spec_parser import parse_oui_table

# Set up an app
app = Webapp(__name__, static_directory="static", google_tracking_code=None)
CACHE_SECONDS = 60

# OUI data remote
OUI_FILE_URL = "http://standards-oui.ieee.org/oui.txt"
OUI_CACHE_FILE = "/tmp/oui.db.txt"

def _get_oui_db() -> str:
    
    # Check if the OUI db file has been pre-downloaded yet
    if not os.path.isfile(OUI_CACHE_FILE):
        print("Downloading and caching OUI database")
        with open(OUI_CACHE_FILE, "w") as fp:
            fp.write(requests.get(OUI_FILE_URL).text)
    
    # Return file contents
    content: str
    with open(OUI_CACHE_FILE, "r") as fp:
        content = fp.read()
        print(f"Using cache to serve OUI database {os.path.expanduser(OUI_CACHE_FILE)} ({len(content)} chars)")
    return content


@app.errorhandler(404)
def page_not_found(e):
    return flask.jsonify({"success": False, "message": "Not found"}), 404


@app.route("/lookup/<oui>")
def lookup(oui: str) -> flask.Response:

    print(f"Got request for OUI: {oui}")

    # Grab a copy of the OUI database
    oui_db = _get_oui_db()

    # Search for entry
    for vendor in parse_oui_table(oui_db):
        if vendor.oui == oui or vendor.company_id == oui:
            res = flask.make_response(flask.jsonify({
                "success": "True",
                "vendor": vendor.__dict__
            }))
            res.headers.set('Cache-Control', f"s-maxage={CACHE_SECONDS}, stale-while-revalidate")
            return res

    # If the OUI id invalid
    res = flask.make_response(flask.jsonify({
        "success": False,
        "message": "OUI invalid or not assigned"
    }), 404)
    res.headers.set('Cache-Control', f"s-maxage={CACHE_SECONDS}, stale-while-revalidate")
    return res


if __name__ == "__main__":
    app.run(debug=True)
