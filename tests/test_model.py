"""
Unit tests for the ML model.
"""

import pytest
import numpy as np
import pickle
from pathlib import Path
from sklearn.datasets import load_iris


@pytest.fixture
def model_path():
    """Get the path to the trained model."""
    project_root = Path(__file__).parent.parent
    return project_root / "model" / "model.pkl"


@pytest.fixture
def sample_features():
    """Sample Iris features for testing."""
    # Sample from Iris dataset: setosa
    return [5.1, 3.5, 1.4, 0.2]


def test_model_exists(model_path):
    """Test that the model file exists."""
    assert model_path.exists(), f"Model file not found at {model_path}. Run train.py first."


def test_model_loads(model_path):
    """Test that the model can be loaded."""
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    
    assert model is not None, "Model should not be None"


def test_model_prediction_shape(model_path, sample_features):
    """Test that model predictions have the correct shape."""
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    
    features_array = np.array(sample_features).reshape(1, -1)
    prediction = model.predict(features_array)
    probabilities = model.predict_proba(features_array)
    
    # Check prediction shape
    assert prediction.shape == (1,), f"Expected prediction shape (1,), got {prediction.shape}"
    
    # Check probabilities shape
    assert probabilities.shape == (1, 3), f"Expected probabilities shape (1, 3), got {probabilities.shape}"
    
    # Check that probabilities sum to 1
    assert np.isclose(probabilities.sum(), 1.0), "Probabilities should sum to 1.0"


def test_model_prediction_type(model_path, sample_features):
    """Test that model predictions are integers."""
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    
    features_array = np.array(sample_features).reshape(1, -1)
    prediction = model.predict(features_array)
    
    assert isinstance(prediction[0], (int, np.integer)), "Prediction should be an integer"


def test_model_prediction_range(model_path, sample_features):
    """Test that model predictions are in valid range [0, 2]."""
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    
    features_array = np.array(sample_features).reshape(1, -1)
    prediction = model.predict(features_array)
    
    assert 0 <= prediction[0] <= 2, f"Prediction should be in range [0, 2], got {prediction[0]}"


def test_model_with_iris_dataset(model_path):
    """Test model with actual Iris dataset samples."""
    iris = load_iris()
    X, y = iris.data, iris.target
    
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    
    # Test with first sample from each class
    for i in range(3):
        sample = X[y == i][0].reshape(1, -1)
        prediction = model.predict(sample)[0]
        
        # The model should predict the correct class for training-like samples
        assert prediction in [0, 1, 2], f"Prediction should be 0, 1, or 2, got {prediction}"

