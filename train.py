"""
Train a simple Iris classifier model using scikit-learn.
This script trains a Random Forest classifier on the Iris dataset
and saves it to model/model.pkl
"""

import os
import pickle
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


def train_model():
    """Train and save the Iris classifier model."""
    # Load the Iris dataset
    print("Loading Iris dataset...")
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train the model
    print("Training Random Forest classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=iris.target_names))
    
    # Create model directory if it doesn't exist
    os.makedirs("model", exist_ok=True)
    
    # Save the model
    model_path = "model/model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    
    print(f"\nModel saved to {model_path}")
    return model


if __name__ == "__main__":
    train_model()

