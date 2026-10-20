"""Flask API for heart disease prediction."""
import logging
import json
from datetime import datetime
from pathlib import Path

from flask import Flask, request, jsonify
import numpy as np
import pandas as pd

from src.models.inference import ModelInference
from src.data.preprocessor import HeartDiseasePreprocessor
from src.models.trainer import ModelTrainer

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global model and preprocessor
model = None
preprocessor = None
inference_engine = None

def load_model_and_preprocessor():
    """Load model and preprocessor from disk."""
    global model, preprocessor, inference_engine

    model_path = Path(__file__).parent.parent.parent / 'models' / 'best_model.pkl'
    preprocessor_path = Path(__file__).parent.parent.parent / 'models' / 'preprocessor.pkl'

    try:
        if model_path.exists():
            model = ModelTrainer.load_model(str(model_path))
            logger.info("✓ Model loaded successfully")
        else:
            logger.warning("⚠ Model file not found")

        if preprocessor_path.exists():
            preprocessor = HeartDiseasePreprocessor.load(str(preprocessor_path))
            logger.info("✓ Preprocessor loaded successfully")
        else:
            logger.warning("⚠ Preprocessor file not found")

        if model and preprocessor:
            inference_engine = ModelInference(model, preprocessor)
            logger.info("✓ Inference engine initialized")

    except Exception as e:
        logger.error(f"Error loading model/preprocessor: {e}")

@app.before_request
def before_request():
    """Log incoming requests."""
    logger.info(f"{request.method} {request.path}")
    if request.is_json:
        logger.debug(f"Payload: {request.get_json()}")

@app.after_request
def after_request(response):
    """Log response."""
    logger.info(f"Response: {response.status_code}")
    return response

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'model_loaded': inference_engine is not None
    }), 200

@app.route('/predict', methods=['POST'])
def predict():
    """
    Prediction endpoint.

    Expected JSON:
    {
        "age": 50,
        "sex": 1,
        "cp": 3,
        "trestbps": 140,
        "chol": 289,
        "fbs": 0,
        "restecg": 0,
        "thalach": 150,
        "exang": 0,
        "oldpeak": 2.2,
        "slope": 1,
        "ca": 0,
        "thal": 2
    }
    """
    if not inference_engine:
        return jsonify({
            'error': 'Model not loaded',
            'status': 'error'
        }), 503

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'error': 'No JSON data provided',
                'status': 'error'
            }), 400

        # Make prediction
        result = inference_engine.predict(data)
        result['status'] = 'success'

        logger.info(f"Prediction made: {result}")
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/metrics', methods=['GET'])
def metrics():
    """Prometheus-compatible metrics endpoint."""
    return jsonify({
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'heart-disease-api',
        'version': '1.0.0'
    }), 200

@app.route('/info', methods=['GET'])
def info():
    """API information endpoint."""
    return jsonify({
        'name': 'Heart Disease Prediction API',
        'version': '1.0.0',
        'description': 'ML-powered heart disease risk prediction',
        'endpoints': [
            {'path': '/health', 'method': 'GET'},
            {'path': '/predict', 'method': 'POST'},
            {'path': '/metrics', 'method': 'GET'},
            {'path': '/info', 'method': 'GET'}
        ]
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found', 'status': 'error'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

if __name__ == '__main__':
    load_model_and_preprocessor()
    app.run(host='0.0.0.0', port=5000, debug=False)
