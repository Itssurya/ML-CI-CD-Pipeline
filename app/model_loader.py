"""
Model loader utility for loading the trained ML model.
"""

import os
import pickle
from pathlib import Path


class ModelLoader:
    """Singleton class to load and manage the ML model."""
    
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance
    
    def load_model(self):
        """Load the trained model from disk."""
        if self._model is None:
            # Get the project root directory
            current_dir = Path(__file__).parent
            project_root = current_dir.parent
            model_path = project_root / "model" / "model.pkl"
            
            if not model_path.exists():
                raise FileNotFoundError(
                    f"Model file not found at {model_path}. "
                    "Please run train.py first to generate the model."
                )
            
            with open(model_path, "rb") as f:
                self._model = pickle.load(f)
            
            print(f"Model loaded successfully from {model_path}")
        
        return self._model
    
    def get_model(self):
        """Get the loaded model instance."""
        if self._model is None:
            self.load_model()
        return self._model

