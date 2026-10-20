# MLOps: Heart Disease Prediction - End-to-End ML Pipeline

## 📋 Project Overview

This is a comprehensive MLOps implementation for heart disease risk prediction using modern best practices including experiment tracking, CI/CD automation, containerization, Kubernetes deployment, and production monitoring.

**Dataset:** UCI Heart Disease Dataset  
**Problem:** Binary classification (presence/absence of heart disease)  
**Total Marks:** 50

## 🎯 Project Structure

```
mlops-heart-disease/
├── data/                          # Dataset storage
│   ├── download_data.py          # Script to download UCI dataset
│   └── heart.csv                 # Raw dataset (in .gitignore)
├── notebooks/                     # Jupyter notebooks
│   ├── 01_eda.ipynb              # Exploratory Data Analysis
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_training.ipynb
├── src/                           # Production code
│   ├── __init__.py
│   ├── data/
│   │   ├── loader.py             # Data loading utilities
│   │   ├── preprocessor.py       # Data preprocessing pipeline
│   │   └── transformers.py       # Custom transformers
│   ├── models/
│   │   ├── trainer.py            # Model training logic
│   │   ├── evaluator.py          # Model evaluation
│   │   └── inference.py          # Prediction logic
│   └── api/
│       ├── app.py                # Flask/FastAPI application
│       ├── routes.py             # API endpoints
│       └── middleware.py         # Logging & monitoring middleware
├── tests/                         # Unit and integration tests
│   ├── test_data.py
│   ├── test_preprocessing.py
│   ├── test_models.py
│   └── test_api.py
├── deployment/                    # Deployment configurations
│   ├── kubernetes/
│   │   ├── deployment.yaml       # K8s deployment
│   │   ├── service.yaml          # K8s service
│   │   └── ingress.yaml          # K8s ingress
│   └── helm/                      # Helm charts (optional)
├── monitoring/                    # Monitoring setup
│   ├── prometheus.yml            # Prometheus config
│   └── grafana_dashboard.json    # Grafana dashboard
├── .github/
│   └── workflows/
│       └── ci_cd.yml             # GitHub Actions CI/CD
├── Dockerfile                     # Container image
├── docker-compose.yml            # Local development stack
├── requirements.txt              # Python dependencies
├── setup.py                      # Package setup
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- Git
- kubectl (for Kubernetes deployment)

### 1. Clone and Setup

```bash
git clone https://github.com/YOUR_USERNAME/mlops-heart-disease.git
cd mlops-heart-disease

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Download Data

```bash
python data/download_data.py
```

### 3. Run EDA & Training

```bash
jupyter notebook notebooks/01_eda.ipynb
jupyter notebook notebooks/02_feature_engineering.ipynb
jupyter notebook notebooks/03_model_training.ipynb
```

### 4. View MLflow Experiments

```bash
mlflow ui --host 127.0.0.1 --port 5001
# Visit http://localhost:5001
```

### 5. Run Tests

```bash
pytest tests/ -v --cov=src
```

### 6. Local Docker Deployment

```bash
docker build -t heart-disease-api:latest .
docker run -p 5000:5000 heart-disease-api:latest

# Test API
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 50, "sex": 1, "cp": 3, "trestbps": 140, ...}'
```

### 7. Full Stack with Docker Compose

```bash
docker-compose up -d

# Access services:
# API: http://localhost:5000
# MLflow: http://localhost:5001
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000
```

## 📊 Tasks & Marks Breakdown

| Task | Description | Marks |
|------|-------------|-------|
| 1 | Data Acquisition & EDA | 5 |
| 2 | Feature Engineering & Models | 8 |
| 3 | Experiment Tracking (MLflow) | 5 |
| 4 | Model Packaging & Reproducibility | 7 |
| 5 | CI/CD Pipeline & Testing | 8 |
| 6 | Docker Containerization | 5 |
| 7 | Production Deployment | 7 |
| 8 | Monitoring & Logging | 3 |
| 9 | Documentation & Report | 2 |
| **Total** | | **50** |

## 🔄 CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/ci_cd.yml`):
- ✅ Linting (Black, Flake8)
- ✅ Unit tests with coverage
- ✅ Model training & validation
- ✅ Artifact storage
- ✅ Docker image build & push

## 📦 Models

- **Logistic Regression:** Fast baseline model
- **Random Forest:** Ensemble model for better performance

Hyperparameters logged in MLflow for reproducibility.

## 🐳 Docker & Kubernetes

### Local Kubernetes (Minikube)

```bash
minikube start
kubectl apply -f deployment/kubernetes/deployment.yaml
kubectl apply -f deployment/kubernetes/service.yaml
kubectl port-forward svc/heart-disease-api 5000:5000
```

### Cloud Deployment (GKE/EKS/AKS)

See documentation for cloud-specific instructions.

## 📈 Monitoring

- **Prometheus:** Metrics collection
- **Grafana:** Visualization & dashboards
- **API Logging:** JSON structured logs

## 📝 API Documentation

### POST /predict
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 50,
    "sex": 1,
    "cp": 3,
    "trestbps": 140,
    "chol": 289,
    "fbs": 0,
    "restecg": 0,
    "thalach": 150,
    "exang": 0,
    "oldpeak": 2.2,
    "slope": 1,
    "ca": 0,
    "thal": 2
  }'
```

**Response:**
```json
{
  "prediction": 1,
  "confidence": 0.87,
  "model_version": "v1.0.0",
  "timestamp": "2024-01-15T10:30:45Z"
}
```

### GET /health
Health check endpoint

### GET /metrics
Prometheus metrics

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html

# Specific test
pytest tests/test_api.py::test_predict_endpoint -v
```

## 📚 Key Technologies

- **ML Framework:** Scikit-Learn
- **Experiment Tracking:** MLflow
- **API Framework:** Flask / FastAPI
- **Containerization:** Docker
- **Orchestration:** Kubernetes
- **Monitoring:** Prometheus + Grafana
- **CI/CD:** GitHub Actions
- **Testing:** Pytest

## 📖 Documentation

See the full 10-page report in `/docs/MLOps_Assignment_Report.pdf` for:
- Architecture diagrams
- Setup instructions
- EDA findings
- Model selection rationale
- Deployment proof
- Performance metrics

## ✅ Academic Integrity

This project demonstrates original implementation of MLOps concepts with personalized:
- Feature engineering approach
- Model architecture decisions
- Monitoring setup
- Deployment strategy
- Documentation

## 🤝 Contributing

This is an assignment submission - modifications after submission will not be accepted.

## 📞 Support

For issues or questions, refer to the assignment specification or course materials.

---

**Last Updated:** 2024-10-20  
**Status:** In Development  
