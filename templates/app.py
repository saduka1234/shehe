from flask import Flask, request, jsonify, render_template
from datetime import datetime
import json

app = Flask(__name__)

# Initial settings and data storage
settings = {
    "interval": 10000,
    "relayHardOn": False
}
tank_height = 18  # Tank height in cm
last_distance = 0
history = []

@app.route('/')
def index():
    return render_template('dashboard.html', tank_height=tank_height)

@app.route('/get_settings', methods=['GET'])
def get_settings():
    return jsonify(settings)

@app.route('/post_distance', methods=['POST'])
def post_distance():
    global last_distance, history
    data = request.get_json()
    last_distance = data.get("distance", 0)
    
    # Store historical data with timestamp
    history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "distance": last_distance,
        "water_level": tank_height - last_distance
    })
    
    # Keep only last 100 entries
    if len(history) > 100:
        history = history[-100:]
    
    return jsonify({"status": "success"})

@app.route('/get_last_distance', methods=['GET'])
def get_last_distance():
    return jsonify({
        "distance": last_distance,
        "water_level": tank_height - last_distance,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/get_history', methods=['GET'])
def get_history():
    return jsonify(history[-24:])  # Return last 24 entries

@app.route('/update_settings', methods=['POST'])
def update_settings():
    global settings
    data = request.get_json()
    settings["interval"] = data.get("interval", settings["interval"])
    settings["relayHardOn"] = data.get("relayHardOn", settings["relayHardOn"])
    return jsonify({"status": "settings updated"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)