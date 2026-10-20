"""Data loading utilities."""
import pandas as pd
from pathlib import Path

def load_data(filepath: str) -> pd.DataFrame:
    """Load heart disease dataset from CSV."""
    df = pd.read_csv(filepath)
    return df

def train_test_split_data(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42):
    """Split data into train and test sets."""
    from sklearn.model_selection import train_test_split

    X = df.drop('target', axis=1)
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    return X_train, X_test, y_train, y_test

def get_feature_names(X: pd.DataFrame) -> list:
    """Get feature names from dataset."""
    return X.columns.tolist()
