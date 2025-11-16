"""
Unit tests for the FastAPI application.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.model_loader import ModelLoader
import os
from pathlib import Path


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def sample_request_data():
    """Sample request data for testing."""
    return {
        "features": [5.1, 3.5, 1.4, 0.2]  # Sample Iris features
    }


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "endpoints" in data


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_loaded" in data


def test_predict_endpoint_success(client, sample_request_data):
    """Test successful prediction."""
    # Ensure model exists
    model_path = Path(__file__).parent.parent / "model" / "model.pkl"
    if not model_path.exists():
        pytest.skip("Model not found. Run train.py first.")
    
    response = client.post("/predict", json=sample_request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "prediction" in data
    assert "prediction_proba" in data
    assert "class_name" in data
    
    # Validate prediction type
    assert isinstance(data["prediction"], int)
    assert 0 <= data["prediction"] <= 2
    
    # Validate probabilities
    assert len(data["prediction_proba"]) == 3
    assert all(isinstance(p, (int, float)) for p in data["prediction_proba"])
    assert abs(sum(data["prediction_proba"]) - 1.0) < 0.01
    
    # Validate class name
    assert data["class_name"] in ["setosa", "versicolor", "virginica"]


def test_predict_endpoint_invalid_features_count(client):
    """Test prediction with invalid number of features."""
    # Too few features
    response = client.post("/predict", json={"features": [5.1, 3.5]})
    assert response.status_code == 422  # Validation error
    
    # Too many features
    response = client.post("/predict", json={"features": [5.1, 3.5, 1.4, 0.2, 0.5]})
    assert response.status_code == 422  # Validation error


def test_predict_endpoint_missing_features(client):
    """Test prediction with missing features field."""
    response = client.post("/predict", json={})
    assert response.status_code == 422  # Validation error


def test_predict_endpoint_invalid_json(client):
    """Test prediction with invalid JSON."""
    response = client.post("/predict", json={"features": "invalid"})
    assert response.status_code == 422  # Validation error


def test_predict_endpoint_different_samples(client):
    """Test prediction with different Iris samples."""
    model_path = Path(__file__).parent.parent / "model" / "model.pkl"
    if not model_path.exists():
        pytest.skip("Model not found. Run train.py first.")
    
    # Test samples from different classes
    test_samples = [
        [5.1, 3.5, 1.4, 0.2],  # setosa
        [7.0, 3.2, 4.7, 1.4],  # versicolor
        [6.3, 3.3, 6.0, 2.5],  # virginica
    ]
    
    for sample in test_samples:
        response = client.post("/predict", json={"features": sample})
        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
        assert "class_name" in data

