from flask import Blueprint, request, jsonify, render_template
from config import PASSWORD
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
    return """Authorized"""