"""Tests for model training and evaluation."""
import pytest
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from src.models.trainer import ModelTrainer
from src.models.evaluator import ModelEvaluator

@pytest.fixture
def sample_data():
    """Create sample classification data."""
    X, y = make_classification(n_samples=100, n_features=13, n_informative=10,
                               n_redundant=2, random_state=42)
    X_train, X_test = X[:80], X[80:]
    y_train, y_test = y[:80], y[80:]

    # Convert to DataFrame for compatibility
    X_train_df = pd.DataFrame(X_train, columns=[f'feature_{i}' for i in range(13)])
    X_test_df = pd.DataFrame(X_test, columns=[f'feature_{i}' for i in range(13)])

    return X_train_df, X_test_df, y_train, y_test

def test_logistic_regression_training(sample_data):
    """Test Logistic Regression training."""
    X_train, X_test, y_train, y_test = sample_data

    trainer = ModelTrainer()
    model, metrics = trainer.train_logistic_regression(X_train, y_train, X_test, y_test)

    assert model is not None
    assert 'accuracy' in metrics
    assert 'precision' in metrics
    assert 'recall' in metrics
    assert metrics['accuracy'] > 0.5

def test_random_forest_training(sample_data):
    """Test Random Forest training."""
    X_train, X_test, y_train, y_test = sample_data

    trainer = ModelTrainer()
    model, metrics = trainer.train_random_forest(X_train, y_train, X_test, y_test)

    assert model is not None
    assert 'accuracy' in metrics
    assert 'roc_auc' in metrics
    assert metrics['accuracy'] > 0.5

def test_model_evaluation(sample_data):
    """Test model evaluation metrics."""
    X_train, X_test, y_train, y_test = sample_data

    trainer = ModelTrainer()
    model, _ = trainer.train_logistic_regression(X_train, y_train, X_test, y_test)

    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    metrics = ModelEvaluator.evaluate(y_test, y_pred, y_pred_proba)

    assert 'accuracy' in metrics
    assert 'f1' in metrics
    assert 'roc_auc' in metrics
    assert 0 <= metrics['accuracy'] <= 1

def test_model_save_load(tmp_path, sample_data):
    """Test model save and load."""
    X_train, X_test, y_train, y_test = sample_data

    trainer = ModelTrainer()
    model, _ = trainer.train_logistic_regression(X_train, y_train, X_test, y_test)

    # Save
    filepath = tmp_path / "model.pkl"
    trainer.save_model(model, str(filepath))

    # Load
    loaded_model = ModelTrainer.load_model(str(filepath))

    # Test both produce same predictions
    y_pred1 = model.predict(X_test)
    y_pred2 = loaded_model.predict(X_test)

    np.testing.assert_array_equal(y_pred1, y_pred2)
