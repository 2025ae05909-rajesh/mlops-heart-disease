"""Tests for API endpoints."""
import pytest
import json
from src.api.app import app

@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get('/health')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_info_endpoint(client):
    """Test info endpoint."""
    response = client.get('/info')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'name' in data
    assert 'version' in data
    assert 'endpoints' in data

def test_predict_endpoint_no_model(client):
    """Test predict endpoint without model loaded."""
    response = client.post('/predict',
                          json={
                              'age': 50,
                              'sex': 1
                          })

    # Should return 503 if model not loaded, or 400 if data invalid
    assert response.status_code in [400, 503]

def test_predict_endpoint_invalid_json(client):
    """Test predict with invalid JSON."""
    response = client.post('/predict',
                          data='invalid',
                          content_type='text/plain')

    assert response.status_code != 200

def test_metrics_endpoint(client):
    """Test metrics endpoint."""
    response = client.get('/metrics')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'timestamp' in data

def test_not_found_endpoint(client):
    """Test 404 error handling."""
    response = client.get('/nonexistent')

    assert response.status_code == 404
