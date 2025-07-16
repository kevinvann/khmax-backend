from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load data once when the server starts
df = pd.read_csv('vehicle_data.csv')

# Normalize column names
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

@app.route('/makes', methods=['GET'])
def get_makes():
    makes = df['make'].dropna().unique().tolist()
    return jsonify(sorted(makes))

@app.route('/models', methods=['GET'])
def get_models():
    make = request.args.get('make')
    if not make:
        return jsonify({'error': 'Missing make parameter'}), 400
    models = df[df['make'] == make]['model'].dropna().unique().tolist()
    return jsonify(sorted(models))

@app.route('/types', methods=['GET'])
def get_types():
    make = request.args.get('make')
    model = request.args.get('model')
    if not make:
        return jsonify({'error': 'Missing make parameter'}), 400
    if not model:
        return jsonify({'error': 'Missing model parameter'}), 400

    filtered = df[(df['make'] == make) & (df['model'] == model)]

    types = filtered['type'].dropna().unique().tolist()

    return jsonify(sorted(types))

@app.route('/countries', methods=['GET'])
def get_countries():
    make = request.args.get('make')
    model = request.args.get('model')
    type = request.args.get('type')
    if not make:
        return jsonify({'error': 'Missing make parameter'}), 400
    if not model:
        return jsonify({'error': 'Missing model parameter'}), 400
    if not type:
        return jsonify({'error': 'Missing type parameter'}), 400

    filtered = df[(df['make'] == make) & (df['model'] == model) & (df['type'] == type)]

    countries = filtered['country'].dropna().unique().tolist()

    return jsonify(sorted(countries))

@app.route('/engines', methods=['GET'])
def get_engines():
    make = request.args.get('make')
    model = request.args.get('model')
    type = request.args.get('type')
    country = request.args.get('country')

    if not make:
        return jsonify({'error': 'Missing make parameter'}), 400
    if not model:
        return jsonify({'error': 'Missing model parameter'}), 400
    if not type:
        return jsonify({'error': 'Missing type parameter'}), 400
    if not country:
        return jsonify({'error': 'Missing country parameter'}), 400

    filtered = df[(df['make'] == make) & (df['model'] == model) & (df['type'] == type) & (df['country'] == country)]

    engines = filtered['engine'].dropna().unique().tolist()

    return jsonify(sorted(engines))

# More endpoints (e.g., years, engines) can follow the same structure

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)