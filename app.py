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
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, sensor_id, value):
        self.sensor_id = sensor_id
        self.value = value
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
    value = data.get('value')

    if sensor_id is None or value is None:
        abort(400)

    sensor_data = SensorData(sensor_id, value)
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
        'value': sensor_data.value,
        'date': sensor_data.date
    })

# Fin de Rutas

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("Tables created")
    app.run(debug=False)