"""Tests for data loading and preprocessing."""
import pytest
import pandas as pd
import numpy as np
from src.data.loader import load_data, train_test_split_data
from src.data.preprocessor import HeartDiseasePreprocessor, handle_missing_values

@pytest.fixture
def sample_dataframe():
    """Create sample heart disease dataset."""
    data = {
        'age': [50, 60, 45, 55, 40, 65, 52, 58, 48, 62],
        'sex': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        'cp': [3, 2, 3, 1, 2, 3, 1, 2, 3, 1],
        'trestbps': [140, 150, 130, 120, 135, 145, 125, 155, 140, 130],
        'chol': [289, 260, 200, 220, 240, 250, 210, 270, 280, 230],
        'fbs': [0, 1, 0, 0, 1, 0, 1, 0, 0, 1],
        'restecg': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        'thalach': [150, 140, 160, 130, 145, 155, 150, 135, 165, 125],
        'exang': [0, 1, 0, 0, 1, 0, 1, 0, 0, 1],
        'oldpeak': [2.2, 1.5, 0.5, 1.0, 2.5, 1.2, 0.8, 1.8, 2.0, 1.5],
        'slope': [1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
        'ca': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        'thal': [2, 3, 2, 1, 2, 3, 2, 1, 3, 2],
        'target': [1, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    }
    return pd.DataFrame(data)

def test_train_test_split(sample_dataframe):
    """Test train-test split."""
    X_train, X_test, y_train, y_test = train_test_split_data(sample_dataframe)

    assert len(X_train) + len(X_test) == len(sample_dataframe)
    assert len(y_train) + len(y_test) == len(sample_dataframe)
    assert X_train.shape[1] == 13  # 14 columns - 1 target

def test_preprocessor_fit_transform(sample_dataframe):
    """Test preprocessor fit and transform."""
    X = sample_dataframe.drop('target', axis=1)

    preprocessor = HeartDiseasePreprocessor()
    X_transformed = preprocessor.fit_transform(X)

    assert X_transformed.shape[0] == X.shape[0]
    assert X_transformed.shape[1] == X.shape[1]

def test_handle_missing_values():
    """Test handling of missing values."""
    data = {
        'age': [50, np.nan, 45],
        'chol': [289, 260, np.nan]
    }
    df = pd.DataFrame(data)

    df_filled = handle_missing_values(df, strategy='mean')

    assert df_filled.isnull().sum().sum() == 0

def test_preprocessor_save_load(tmp_path, sample_dataframe):
    """Test preprocessor save and load."""
    X = sample_dataframe.drop('target', axis=1)

    preprocessor = HeartDiseasePreprocessor()
    preprocessor.fit(X)

    # Save
    filepath = tmp_path / "preprocessor.pkl"
    preprocessor.save(str(filepath))

    # Load
    loaded_preprocessor = HeartDiseasePreprocessor.load(str(filepath))

    # Test both produce same output
    X_transformed1 = preprocessor.transform(X)
    X_transformed2 = loaded_preprocessor.transform(X)

    np.testing.assert_array_almost_equal(X_transformed1, X_transformed2)
