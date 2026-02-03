from flask import Blueprint, request, jsonify
import config.extensions as extensions
from services.actuator_service import send_actuator_command

bp = Blueprint("actuators", __name__, url_prefix="/api/v1/actuators")


@bp.post("/<name>/set")
def set_actuator(name: str):
    payload = request.get_json(silent=True)
    if not payload or "state" not in payload:
        return {"error": "Missing state"}, 400

    send_actuator_command(name, bool(payload["state"]))
    return jsonify({"status": "sent"}), 202
