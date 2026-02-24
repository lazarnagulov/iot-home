from typing import Dict, List
from flask import Blueprint, jsonify, render_template

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