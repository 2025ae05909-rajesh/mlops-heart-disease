"""
Download Heart Disease UCI Dataset

Source: https://archive.ics.uci.edu/ml/datasets/heart+disease
"""
import os
import pandas as pd
import urllib.request
from pathlib import Path

def download_heart_disease_dataset(output_dir='data'):
    """Download the Heart Disease dataset from UCI repository."""

    os.makedirs(output_dir, exist_ok=True)

    # UCI Heart Disease dataset URL
    url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data'

    # Column names as per UCI documentation
    columns = [
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
        'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target'
    ]

    output_path = os.path.join(output_dir, 'heart.csv')

    try:
        print(f"Downloading Heart Disease dataset from {url}...")
        urllib.request.urlretrieve(url, 'temp_heart.data')

        # Load data with ? as missing value indicator
        df = pd.read_csv('temp_heart.data', names=columns, na_values='?')

        # Convert target to binary (>0 = 1, 0 = 0)
        df['target'] = (df['target'] > 0).astype(int)

        # Save to CSV
        df.to_csv(output_path, index=False)
        print(f"✓ Dataset saved to {output_path}")

        # Display dataset info
        print(f"\nDataset shape: {df.shape}")
        print(f"Missing values:\n{df.isnull().sum()}")
        print(f"\nTarget distribution:\n{df['target'].value_counts()}")

        # Clean up temp file
        if os.path.exists('temp_heart.data'):
            os.remove('temp_heart.data')

        return df

    except Exception as e:
        print(f"✗ Error downloading dataset: {e}")
        print("\nAlternative: Download manually from https://archive.ics.uci.edu/ml/datasets/heart+disease")
        return None

if __name__ == "__main__":
    df = download_heart_disease_dataset()
    if df is not None:
        print("\n✓ Dataset download successful!")
    else:
        print("\n✗ Dataset download failed!")
