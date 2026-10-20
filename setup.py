from setuptools import setup, find_packages

setup(
    name="mlops-heart-disease",
    version="1.0.0",
    description="MLOps End-to-End Pipeline for Heart Disease Prediction",
    author="MLOps Student",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "pandas>=2.0.0",
        "scikit-learn>=1.3.0",
        "mlflow>=2.7.0",
        "flask>=2.3.0",
        "fastapi>=0.103.0",
        "pytest>=7.4.0",
    ],
)
