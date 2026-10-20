.PHONY: help install data test lint train docker-build docker-run deploy clean

help:
	@echo "MLOps Heart Disease Prediction - Available Commands"
	@echo "===================================================="
	@echo "  make install        - Install dependencies"
	@echo "  make data           - Download dataset"
	@echo "  make train          - Train models"
	@echo "  make test           - Run tests"
	@echo "  make lint           - Run linters"
	@echo "  make docker-build   - Build Docker image"
	@echo "  make docker-run     - Run Docker container"
	@echo "  make docker-compose - Start full stack"
	@echo "  make clean          - Clean artifacts"

install:
	pip install -r requirements.txt

data:
	python data/download_data.py

train:
	python train.py

test:
	pytest tests/ -v --cov=src

lint:
	black src/ tests/
	flake8 src/ tests/
	pylint src/ --disable=all --enable=E,F

docker-build:
	docker build -t heart-disease-api:latest .

docker-run:
	docker run -p 5000:5000 heart-disease-api:latest

docker-compose:
	docker-compose up -d

docker-logs:
	docker-compose logs -f api

docker-down:
	docker-compose down

mlflow:
	mlflow ui --host 127.0.0.1 --port 5001

kubernetes-deploy:
	kubectl apply -f deployment/kubernetes/deployment.yaml
	kubectl apply -f deployment/kubernetes/service.yaml
	kubectl apply -f deployment/kubernetes/hpa.yaml

kubernetes-check:
	kubectl get deployments
	kubectl get services
	kubectl get pods

clean:
	rm -rf __pycache__ .pytest_cache .coverage htmlcov
	rm -rf models/*.pkl mlruns/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
