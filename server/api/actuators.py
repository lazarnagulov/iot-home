from flask import Blueprint, request, jsonify
import config.extensions as extensions
from services.actuator_service import send_actuator_command

bp = Blueprint("actuators", __name__, url_prefix="/api/v1/actuators")


@bp.post("/<name>/toggle")
def set_actuator(name: str):
    send_actuator_command(name)
    return jsonify({"status": "sent"}), 202
