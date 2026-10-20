# Deployment Guide - Heart Disease Prediction API

## Local Development

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- Git

### Quick Start (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/mlops-heart-disease.git
cd mlops-heart-disease

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download data
python data/download_data.py

# 5. Train models
python train.py

# 6. Run tests
pytest tests/ -v

# 7. View MLflow
mlflow ui --port 5001
# Visit http://localhost:5001

# 8. Start full stack
docker-compose up -d

# 9. Test API
curl http://localhost:5000/health

# 10. Stop stack
docker-compose down
```

## Docker Deployment

### Build Docker Image

```bash
docker build -t heart-disease-api:v1.0.0 .
```

### Run Docker Container

```bash
docker run -d \
  -p 5000:5000 \
  --name heart-disease-api \
  -e FLASK_ENV=production \
  heart-disease-api:v1.0.0
```

### Test Container

```bash
# Health check
curl http://localhost:5000/health

# Make prediction
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

## Kubernetes Deployment

### Prerequisites
- Kubectl installed
- Kubernetes cluster (Minikube, EKS, GKE, AKS)
- Docker image pushed to registry

### Deploy to Kubernetes

```bash
# 1. Create namespace
kubectl create namespace mlops

# 2. Apply deployments
kubectl apply -f deployment/kubernetes/deployment.yaml
kubectl apply -f deployment/kubernetes/service.yaml
kubectl apply -f deployment/kubernetes/hpa.yaml -n mlops

# 3. Check status
kubectl get deployments -n mlops
kubectl get pods -n mlops
kubectl get svc -n mlops

# 4. Port forward to local machine
kubectl port-forward svc/heart-disease-api 5000:80 -n mlops

# 5. Test API
curl http://localhost:5000/health
```

### Local Kubernetes (Minikube)

```bash
# 1. Start Minikube
minikube start

# 2. Build image in Minikube
eval $(minikube docker-env)
docker build -t heart-disease-api:latest .

# 3. Deploy
kubectl apply -f deployment/kubernetes/deployment.yaml

# 4. Forward ports
kubectl port-forward svc/heart-disease-api 5000:80

# 5. Test
curl http://localhost:5000/health

# 6. View dashboard
minikube dashboard
```

## Cloud Deployment

### Google Cloud (GKE)

```bash
# 1. Create GKE cluster
gcloud container clusters create mlops-cluster \
  --zone us-central1-a \
  --num-nodes 3

# 2. Push image to GCR
docker tag heart-disease-api:v1.0.0 gcr.io/PROJECT_ID/heart-disease-api:v1.0.0
docker push gcr.io/PROJECT_ID/heart-disease-api:v1.0.0

# 3. Update deployment YAML with GCR image

# 4. Deploy
kubectl apply -f deployment/kubernetes/deployment.yaml

# 5. Expose service
kubectl expose deployment heart-disease-api \
  --type LoadBalancer \
  --port 80 \
  --target-port 5000

# 6. Get external IP
kubectl get service heart-disease-api
```

### AWS (EKS)

```bash
# 1. Create EKS cluster
eksctl create cluster --name mlops-cluster --region us-east-1

# 2. Push image to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

docker tag heart-disease-api:v1.0.0 \
  123456789.dkr.ecr.us-east-1.amazonaws.com/heart-disease-api:v1.0.0

docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/heart-disease-api:v1.0.0

# 3. Deploy
kubectl apply -f deployment/kubernetes/deployment.yaml

# 4. Check service
kubectl get svc
```

## Monitoring & Logging

### Prometheus + Grafana Stack

```bash
# Start with docker-compose
docker-compose up -d prometheus grafana

# Access
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin)
```

### View Logs

```bash
# Docker logs
docker logs -f heart-disease-api

# Kubernetes logs
kubectl logs deployment/heart-disease-api -f
kubectl logs -p pod/PODNAME  # Previous terminated pod
```

## Production Checklist

- [ ] Models trained and validated
- [ ] Tests passing (pytest tests/)
- [ ] Docker image builds successfully
- [ ] API health check passing
- [ ] Predictions returning expected format
- [ ] Monitoring/alerting configured
- [ ] Logging configured
- [ ] Load testing completed
- [ ] Security review done (no hardcoded secrets)
- [ ] API documentation complete
- [ ] Backup/disaster recovery plan
- [ ] Runbook documentation

## Troubleshooting

### API not responding

```bash
# Check container status
docker ps

# View logs
docker logs heart-disease-api

# Test health endpoint
curl http://localhost:5000/health
```

### Model loading issues

```bash
# Verify model file exists
ls -la models/

# Check file permissions
chmod 644 models/best_model.pkl

# Verify file is not corrupted
python -c "import joblib; joblib.load('models/best_model.pkl')"
```

### Kubernetes pod crashing

```bash
# Check pod logs
kubectl logs pod/PODNAME

# Describe pod for events
kubectl describe pod PODNAME

# Check resource limits
kubectl describe deployment heart-disease-api
```

## Performance Tuning

### API Response Time

- Increase worker threads in Flask/Gunicorn
- Use caching for frequent predictions
- Profile code with `cProfile`

### Memory Optimization

- Use model quantization
- Implement prediction batching
- Monitor with `memory_profiler`

### Scalability

- Adjust HPA thresholds in hpa.yaml
- Increase number of replicas
- Use load balancer
- Implement circuit breaker pattern

## Backup & Recovery

```bash
# Backup models
tar -czf models_backup.tar.gz models/

# Backup MLflow data
docker cp mlflow_mlflow_1:/mlflow mlflow_backup

# Restore
tar -xzf models_backup.tar.gz
```

## References

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Flask Deployment](https://flask.palletsprojects.com/deployment/)
- [MLflow Tracking](https://mlflow.org/docs/latest/tracking.html)
