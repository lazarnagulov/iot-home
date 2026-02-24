from typing import Dict, List
from flask import Blueprint, jsonify, render_template, request

import config.extensions as extensions
from managers.person_count_manager import PersonCountManager
from services.sensor_cache import CacheItem

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def index():
    return render_template('dashboard.html')

@bp.route('/grafana')
def grafana():
    return render_template('grafana.html')


@bp.get('/api/v1/actuators/cards')
def actuators_cards():
    actuators: Dict[str, CacheItem] = extensions.sensor_cache.get_all()
    actuator_cards: List[str] = []    

    for actuator_id, data in actuators.items():
        common_data = {
            'actuator_id': actuator_id,
            'name': data.name,
            'is_simulated': data.is_simulated,
            **data.value
        }
        
        if data.sensor_type == 'diode':
            card_html = render_template('partials/diode_actuator_card.html',
                **common_data
            )
            actuator_cards.append(card_html)
        elif data.sensor_type == "buzzer":
            card_html = render_template('partials/buzzer_actuator_card.html',
                **common_data
            )
            actuator_cards.append(card_html)
        elif data.sensor_type == 'lcd':
            card_html = render_template('partials/lcd_actuator_card.html',
                **common_data
            )
            actuator_cards.append(card_html)
        elif data.sensor_type == '7_segment_display':
            card_html = render_template('partials/4sd_actuator_card.html',
                **common_data
            )
            actuator_cards.append(card_html)
    
    return '<div class="space-y-3">' + ''.join(actuator_cards) + '</div>'


@bp.get('/api/v1/sensors/cards')
def sensors_cards():
    sensors: Dict[str, CacheItem] = extensions.sensor_cache.get_all()
    sensor_cards: List[str] = []    

    for sensor_id, data in sensors.items():
        common_data = {
            'sensor_id': sensor_id,
            'name': data.name,
            'is_simulated': data.is_simulated,
        }
        
        if data.name.startswith("Door Sensor") or data.sensor_id.startswith("ds"):
            card_html = render_template('partials/door_sensor_card.html',
                unlocked=data.value.get('pressed', False),
                **common_data
            )
            sensor_cards.append(card_html)
        elif data.sensor_type == 'ultrasonic':
            card_html = render_template('partials/ultrasonic_sensor_card.html',
                distance=data.value.get('distance', 0),
                **common_data
            )
            sensor_cards.append(card_html)
        elif data.sensor_type == "pir":
            card_html = render_template('partials/pir_sensor_card.html',
                motion_detected=data.value.get('motion', False),
                **common_data
            )
            sensor_cards.append(card_html)
        elif data.sensor_type == 'dht':
            card_html = render_template('partials/temperature_sensor_card.html',
                temperature=data.value.get('temperature', 0),
                humidity=data.value.get('humidity', 0),
                **common_data
            )
            sensor_cards.append(card_html)
        elif data.sensor_type == 'button':
            card_html = render_template('partials/button_sensor_card.html',
                pressed=data.value.get('pressed', False),
                **common_data
            )
            sensor_cards.append(card_html)
        elif data.sensor_type == 'membrane_switch':
            card_html = render_template('partials/membrane_switch_card.html',
                last_key=data.value.get('last_key', '-'),
                **common_data
            )
            sensor_cards.append(card_html) 
        elif data.sensor_type == 'gyro':
            card_html = render_template('partials/gyroscope_sensor_card.html',
                value=data.value,
                **common_data
            )
            sensor_cards.append(card_html)  
    
    return '<div class="space-y-3">' + ''.join(sensor_cards) + '</div>'

@bp.get('/api/v1/people/status')
def people_status():
    return jsonify({"count": PersonCountManager.person_count})

@bp.get('/api/v1/rgb/color')
def rgb_state():
    if extensions.rgb_service is not None:
        return jsonify({
            "r": extensions.rgb_service.r,
            "g": extensions.rgb_service.g,
            "b": extensions.rgb_service.b
        })
    return jsonify({"error": "RGB service not initialized"}), 500

@bp.post('/api/v1/rgb/color')
def set_rgb_color():
    if extensions.rgb_service is None:
        return jsonify({"error": "RGB service not initialized"}), 500
    
    r = request.json.get("r", 0)
    g = request.json.get("g", 0)
    b = request.json.get("b", 0)
    extensions.rgb_service.update_color(r, g, b)
    return jsonify({"success": True})