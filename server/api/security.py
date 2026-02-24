from flask import Blueprint, jsonify, request
from services.actuator_service import send_actuator_command
import threading

import config.extensions as extensions
import config.settings as settings

bp = Blueprint("security", __name__, url_prefix="/api/v1")


@bp.get("/alarm/state")
def get_alarm_state():
    if extensions.alarm_service is None:
        return jsonify({"error": "Alarm service not initialized"}), 500
    else:
        return jsonify({"state": extensions.alarm_service.alarm_state.value}), 200

@bp.post("/security/activate")
def activate_security():
    pin = request.json.get("pin")
    if extensions.alarm_service is None:
        return jsonify({"error": "Alarm service not initialized"}), 500
    if pin != settings.Config.SECURITY_PIN:
        return jsonify({"error": "Invalid PIN"}), 403
    
    extensions.alarm_service.arm()
    return jsonify({"valid": True}), 202

@bp.post("/security/deactivate")
def deactivate_security():
    pin = request.json.get("pin")
    if extensions.alarm_service is None:
        return jsonify({"error": "Alarm service not initialized"}), 500
    if pin != settings.Config.SECURITY_PIN:
        return jsonify({"error": "Invalid PIN"}), 403
    
    extensions.alarm_service.disarm()
    return jsonify({"valid": True}), 202

@bp.post("/alarm/trigger")
def trigger_alarm():
    pin = request.json.get("pin")
    if extensions.alarm_service is None:
        return jsonify({"error": "Alarm service not initialized"}), 500
    if pin != settings.Config.SECURITY_PIN:
        return jsonify({"error": "Invalid PIN"}), 403
    
    extensions.alarm_service.trigger()
    return jsonify({"valid": True}), 202
