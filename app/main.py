"""
FastAPI application for ML model prediction API.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
import numpy as np
from app.model_loader import ModelLoader

# Initialize model loader
model_loader = ModelLoader()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown."""
    # Startup
    try:
        model_loader.load_model()
        print("Model loaded successfully on startup")
    except FileNotFoundError as e:
        print(f"Warning: {e}")
        print("Model will be loaded on first prediction request")
    yield
    # Shutdown (if needed in the future)
    pass


app = FastAPI(
    title="ML Model API",
    description="API for Iris classifier predictions",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS to allow requests from browser (including file://)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictionRequest(BaseModel):
    """Request model for prediction endpoint."""
    features: List[float] = Field(
        ...,
        description="List of 4 features: [sepal_length, sepal_width, petal_length, petal_width]",
        min_length=4,
        max_length=4
    )


class PredictionResponse(BaseModel):
    """Response model for prediction endpoint."""
    prediction: int = Field(..., description="Predicted class (0: setosa, 1: versicolor, 2: virginica)")
    prediction_proba: List[float] = Field(..., description="Prediction probabilities for each class")
    class_name: str = Field(..., description="Name of the predicted class")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "ML Model API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict",
            "health": "/health",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    try:
        model = model_loader.get_model()
        return {
            "status": "healthy",
            "model_loaded": model is not None
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@app.get("/predict")
async def predict_get():
    """
    GET endpoint for /predict - shows usage instructions.
    Use POST method to make predictions.
    """
    return {
        "message": "This endpoint requires POST method",
        "usage": {
            "method": "POST",
            "url": "/predict",
            "headers": {
                "Content-Type": "application/json"
            },
            "body": {
                "features": [5.1, 3.5, 1.4, 0.2]
            },
            "example_curl": "curl -X POST 'http://127.0.0.1:8001/predict' -H 'Content-Type: application/json' -d '{\"features\": [5.1, 3.5, 1.4, 0.2]}'",
            "interactive_docs": "/docs"
        },
        "note": "Visit /docs for interactive API documentation"
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Predict the Iris class based on input features.
    
    Expected features:
    - sepal_length: float
    - sepal_width: float
    - petal_length: float
    - petal_width: float
    """
    try:
        # Load model if not already loaded
        model = model_loader.get_model()
        
        # Validate input
        if len(request.features) != 4:
            raise HTTPException(
                status_code=400,
                detail="Exactly 4 features are required: [sepal_length, sepal_width, petal_length, petal_width]"
            )
        
        # Convert to numpy array and reshape for prediction
        features_array = np.array(request.features).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(features_array)[0]
        prediction_proba = model.predict_proba(features_array)[0].tolist()
        
        # Map class index to class name
        class_names = ["setosa", "versicolor", "virginica"]
        class_name = class_names[prediction]
        
        return PredictionResponse(
            prediction=int(prediction),
            prediction_proba=prediction_proba,
            class_name=class_name
        )
    
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Model not found. Please ensure the model has been trained: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )

