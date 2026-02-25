from flask import Blueprint, jsonify, request
import config.extensions as extensions

bp = Blueprint("kitchen-timer", __name__, url_prefix="/api/v1/kitchen-timer")

@bp.post("/set")
def set_timer():
    service = extensions.kitech_timer_service

    data = request.json or {}
    time = int(data.get("time", 0))
    increment = int(data.get("increment", 10))

    service.set_timer(time, increment)

    return jsonify({"valid": True}), 202
    

@bp.post("/reset")
def reset_timer():
    service = extensions.kitech_timer_service
    service.reset_timer()

    return jsonify({"valid": True}), 202


@bp.post("/btn-press")
def add_time():
    service = extensions.kitech_timer_service
    service.btn_press()

    return jsonify({"valid": True}), 202

@bp.get("/status")
def get_status():
    service = extensions.kitech_timer_service

    return jsonify({
        "remaining": service.remaining,
        "running": service.running,
        "blinking": service.blinking,
        "increment": service.increment
    }), 200    
