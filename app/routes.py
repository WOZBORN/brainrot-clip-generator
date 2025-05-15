from flask import Blueprint, request, jsonify, render_template, url_for
from google_auth_oauthlib.flow import Flow

from config import PASSWORD, CLIENT_SECRETS_FILE, SCOPES, TOKEN_PATH
from .scheduler import start_scheduler, stop_scheduler
from upload.upload_shorts import get_authenticated_service


bp = Blueprint("scheduler", __name__)


@bp.route("/", methods=["GET"])
def index():
    auth = get_authenticated_service()
    return render_template("index.html", auth=auth)


@bp.route("/start", methods=["POST"])
def start():
    data = request.get_json() or {}
    if data.get("password") != PASSWORD:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        start_scheduler()
        return jsonify({"status": "Scheduler started"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/stop", methods=["POST"])
def stop():
    data = request.get_json() or {}
    if data.get("password") != PASSWORD:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        stop_scheduler()
        return jsonify({"status": "Scheduler stopped"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/success", methods=["GET"])
def success():
    code = request.args.get('code')
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('scheduler.success', _external=True)
    )
    flow.fetch_token(code=code)
    creds = flow.credentials
    with open(TOKEN_PATH, 'w') as token_file:
        token_file.write(creds.to_json())
    return 'Authorized'