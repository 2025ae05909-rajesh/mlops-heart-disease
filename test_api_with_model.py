"""
Test API with model loaded
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.models.inference import ModelInference
from src.models.trainer import ModelTrainer
from src.data.preprocessor import HeartDiseasePreprocessor
import joblib

print("\n" + "="*80)
print("Testing API with Trained Model")
print("="*80)

# Load model and preprocessor
model_path = Path("models/best_model.pkl")
preprocessor_path = Path("models/preprocessor.pkl")

print("\n[Loading] Model and Preprocessor...")
model = joblib.load(model_path)
preprocessor = HeartDiseasePreprocessor.load(str(preprocessor_path))
print("[OK] Model loaded:", type(model).__name__)
print("[OK] Preprocessor loaded")

# Create inference engine
inference = ModelInference(model, preprocessor)

# Test data
test_input = {
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

print("\n[Test] Making Prediction...")
print(f"Input: {test_input}")

result = inference.predict(test_input)

print(f"\n[OK] Prediction Result:")
print(f"  Prediction: {result['prediction']} (1=Disease, 0=No Disease)")
print(f"  Confidence: {result['confidence']:.4f}")
print(f"  Model Version: {result['model_version']}")
print(f"  Timestamp: {result['timestamp']}")

# Interpret result
disease_prob = result['confidence'] if result['prediction'] == 1 else (1 - result['confidence'])
print(f"\n[RESULT] Disease Probability: {disease_prob:.2%}")

if result['prediction'] == 1:
    print("[WARNING] High risk of heart disease detected!")
else:
    print("[OK] Low risk - No heart disease detected")

print("\n" + "="*80)
print("API with Model Working Successfully!")
print("="*80 + "\n")
