"""Data preprocessing pipeline."""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import joblib
from pathlib import Path

class HeartDiseasePreprocessor:
    """Preprocessing pipeline for heart disease data."""

    def __init__(self):
        self.preprocessor = None
        self.feature_names = None

    def fit(self, X: pd.DataFrame):
        """Fit preprocessor on training data."""
        # Numerical features to scale
        numerical_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

        self.feature_names = numerical_features

        # Pipeline for numerical features
        numerical_transformer = Pipeline(steps=[
            ('scaler', StandardScaler())
        ])

        # Combine preprocessors
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, numerical_features)
            ],
            remainder='passthrough'
        )

        self.preprocessor.fit(X)
        return self

    def transform(self, X: pd.DataFrame) -> np.ndarray:
        """Transform data."""
        if self.preprocessor is None:
            raise ValueError("Preprocessor not fitted. Call fit() first.")
        return self.preprocessor.transform(X)

    def fit_transform(self, X: pd.DataFrame) -> np.ndarray:
        """Fit and transform data."""
        self.fit(X)
        return self.transform(X)

    def save(self, filepath: str):
        """Save preprocessor to disk."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, filepath)

    @staticmethod
    def load(filepath: str):
        """Load preprocessor from disk."""
        return joblib.load(filepath)

def handle_missing_values(df: pd.DataFrame, strategy: str = 'mean') -> pd.DataFrame:
    """Handle missing values in the dataset."""
    if strategy == 'mean':
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    elif strategy == 'drop':
        df = df.dropna()

    return df

def encode_categorical_features(df: pd.DataFrame) -> pd.DataFrame:
    """Encode categorical features."""
    categorical_cols = df.select_dtypes(include=['object']).columns

    for col in categorical_cols:
        encoder = LabelEncoder()
        df[col] = encoder.fit_transform(df[col].astype(str))

    return df
