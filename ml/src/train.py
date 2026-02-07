"""
Train the parking prediction model
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import joblib
import json
from datetime import datetime

from config import MODEL_PARAMS, MODEL_PATH, FEATURE_NAMES
from features import create_training_dataset


def load_data():
    """Load historical parking data and events"""
    print("Loading data...")
    
    # Get paths relative to script location
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ml_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(ml_dir, 'data', 'processed')
    
    # Load parking data
    parking_path = os.path.join(data_dir, 'parking_data.json')
    parking_df = pd.read_json(parking_path)
    parking_df['datetime'] = pd.to_datetime(parking_df['datetime'])
    
    # Load events - use json.load to preserve list types
    import json
    events_path = os.path.join(data_dir, 'events.json')
    with open(events_path, 'r') as f:
        events_data = json.load(f)
    events_df = pd.DataFrame(events_data)
    
    print(f"Loaded {len(parking_df)} parking records")
    print(f"Loaded {len(events_df)} events")
    
    return parking_df, events_df


def train_model(X_train, y_train):
    """Train Random Forest model"""
    print("\nTraining Random Forest model...")
    print(f"Training samples: {len(X_train)}")
    print(f"Features: {len(FEATURE_NAMES)}")
    print(f"Model parameters: {MODEL_PARAMS}")
    
    model = RandomForestRegressor(**MODEL_PARAMS)
    model.fit(X_train, y_train)
    
    print("Training complete!")
    return model


def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    print("\nEvaluating model...")
    
    y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nModel Performance:")
    print(f"  MAE:  {mae:.4f} ({mae*100:.2f}% error)")
    print(f"  RMSE: {rmse:.4f}")
    print(f"  R²:   {r2:.4f} ({r2*100:.1f}% variance explained)")
    
    # For a 20-space zone
    print(f"\nFor a 20-space parking zone:")
    print(f"  Average error: ~{mae * 20:.1f} spaces")
    
    return {
        'mae': float(mae),
        'rmse': float(rmse),
        'r2': float(r2)
    }


def get_feature_importance(model):
    """Get and display feature importance"""
    print("\nFeature Importance:")
    
    importances = model.feature_importances_
    feature_importance = list(zip(FEATURE_NAMES, importances))
    feature_importance.sort(key=lambda x: x[1], reverse=True)
    
    for i, (feature, importance) in enumerate(feature_importance, 1):
        print(f"  {i:2d}. {feature:25s} {importance:.4f} ({importance*100:.1f}%)")
    
    return dict(feature_importance)


def save_model(model, metrics, feature_importance):
    """Save trained model and metadata"""
    print(f"\nSaving model to {MODEL_PATH}...")
    
    # Get absolute path
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ml_dir = os.path.dirname(script_dir)
    models_dir = os.path.join(ml_dir, 'models')
    
    # Ensure directory exists
    os.makedirs(models_dir, exist_ok=True)
    
    # Save model
    model_file = os.path.join(models_dir, 'parking_model.pkl')
    joblib.dump(model, model_file)
    print(f"Model saved: {model_file}")
    
    # Save metadata
    metadata = {
        'trained_at': datetime.now().isoformat(),
        'model_type': 'RandomForestRegressor',
        'model_params': MODEL_PARAMS,
        'features': FEATURE_NAMES,
        'metrics': metrics,
        'feature_importance': feature_importance
    }
    
    metadata_file = os.path.join(models_dir, 'model_metadata.json')
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"Metadata saved: {metadata_file}")


def main():
    """Main training pipeline"""
    print("="*60)
    print("PARKING PREDICTION MODEL TRAINING")
    print("="*60)
    
    # Load data
    parking_df, events_df = load_data()
    
    # Create features
    print("\nCreating features...")
    X, y = create_training_dataset(parking_df, events_df)
    
    # Split data
    print(f"\nSplitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Training set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    # Train model
    model = train_model(X_train, y_train)
    
    # Evaluate
    metrics = evaluate_model(model, X_test, y_test)
    
    # Feature importance
    feature_importance = get_feature_importance(model)
    
    # Save
    save_model(model, metrics, feature_importance)
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)
    print(f"\nModel file: {MODEL_PATH}parking_model.pkl")
    print(f"Ready to use for predictions!")


if __name__ == "__main__":
    main()
