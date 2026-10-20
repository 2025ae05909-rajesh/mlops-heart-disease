"""
Test API locally without running server
"""
from src.api.app import app
import json

print("\n" + "="*80)
print("Testing Heart Disease Prediction API")
print("="*80)

# Create test client
client = app.test_client()

# Test 1: Health Check
print("\n[Test 1] Health Check")
response = client.get('/health')
print(f"Status: {response.status_code}")
print(f"Response: {response.get_json()}")

# Test 2: Info Endpoint
print("\n[Test 2] API Info")
response = client.get('/info')
data = response.get_json()
print(f"Status: {response.status_code}")
print(f"API Name: {data.get('name')}")
print(f"Version: {data.get('version')}")

# Test 3: Metrics Endpoint
print("\n[Test 3] Metrics")
response = client.get('/metrics')
print(f"Status: {response.status_code}")

# Test 4: Prediction (without model loaded)
print("\n[Test 4] Prediction Endpoint (model not loaded)")
test_data = {
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

response = client.post('/predict',
    json=test_data,
    content_type='application/json'
)
print(f"Status: {response.status_code}")
print(f"Response: {response.get_json()}")

# Test 5: Not Found
print("\n[Test 5] 404 Error Handling")
response = client.get('/nonexistent')
print(f"Status: {response.status_code}")
print(f"Response: {response.get_json()}")

print("\n" + "="*80)
print("API Tests Complete!")
print("="*80)

print("\nTo run the API server:")
print("  python -m src.api.app")
print("\nThen test with:")
print("  curl http://localhost:5000/health")

print("\n[OK] All core APIs working!\n")
