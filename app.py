from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
import os
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import date, timedelta
from sqlalchemy import cast, Date, func

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Inicializar Flask-Migrate

BASE_URL = '/api/'

# Modelos

class SensorData (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, nullable=False)
    soundValue = db.Column(db.Float, nullable=False)
    temperatureValue = db.Column(db.Float, nullable=False)
    humidityValue = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, sensor_id, soundValue, temperatureValue, humidityValue):
        self.sensor_id = sensor_id
        self.soundValue = soundValue
        self.temperatureValue = temperatureValue
        self.humidityValue = humidityValue
        
        self.date = datetime.now()

    def __repr__(self):
        return f'<SensorData {self.sensor_id}>'
    

# Rutas

#ruta default

@app.route('/')
def index():
    return "API de sensores"

@app.route(BASE_URL + 'sensordata', methods=['POST'])
def post_sensor_data():
    data = request.json

    sensor_id = data.get('sensor_id')
    soundValue = data.get('soundValue')
    temperatureValue = data.get('temperatureValue')
    humidityValue = data.get('humidityValue')

    if sensor_id is None or soundValue is None or temperatureValue is None or humidityValue is None:
        abort(400)

    sensor_data = SensorData(sensor_id, soundValue, temperatureValue, humidityValue)
    db.session.add(sensor_data)
    db.session.commit()

    return jsonify({'message': 'Data added successfully'})

@app.route(BASE_URL + 'sensordata/<int:sensor_id>', methods=['GET'])
def get_sensor_data(sensor_id):
    sensor_data = SensorData.query.filter_by(sensor_id=sensor_id).order_by(SensorData.date.desc()).first()

    if sensor_data is None:
        abort(404)

    return jsonify({
        'sensor_id': sensor_data.sensor_id,
        'soundValue': sensor_data.soundValue,
        'temperatureValue': sensor_data.temperatureValue,
        'humidityValue': sensor_data.humidityValue,
        'date': sensor_data.date
    })

#Get Sensor History
@app.route(BASE_URL + 'sensordata/history/<int:sensor_id>', methods=['GET'])
def get_sensor_data_history(sensor_id):
    sensor_data = SensorData.query.filter_by(sensor_id=sensor_id).order_by(SensorData.date.desc()).all()

    if sensor_data is None:
        abort(404)

    return jsonify([{
        'sensor_id': data.sensor_id,
        'soundValue': data.soundValue,
        'temperatureValue': data.temperatureValue,
        'humidityValue': data.humidityValue,
        'date': data.date
    } for data in sensor_data])

# Fin de Rutas

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("Tables created")
    app.run(debug=False)