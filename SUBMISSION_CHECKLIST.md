# Submission Checklist - MLOps Assignment

Use this checklist to verify everything is ready before submission.

## ✅ Core Components

### Data & EDA (5 marks)
- [ ] `data/download_data.py` exists and downloads UCI dataset
- [ ] `notebooks/01_eda.ipynb` contains:
  - [ ] Data loading and cleaning
  - [ ] Missing value analysis
  - [ ] Feature distributions (histograms)
  - [ ] Correlation heatmap
  - [ ] Class balance analysis
  - [ ] Statistical summary
- [ ] Run: `python data/download_data.py` → creates `data/heart.csv`

### Feature Engineering & Models (8 marks)
- [ ] `src/data/preprocessor.py` implements:
  - [ ] StandardScaler for features
  - [ ] Missing value handling
  - [ ] save/load methods
- [ ] `src/models/trainer.py` implements:
  - [ ] Logistic Regression training
  - [ ] Random Forest training
  - [ ] Hyperparameter tuning (GridSearchCV)
  - [ ] MLflow logging
- [ ] `src/models/evaluator.py` calculates:
  - [ ] Accuracy, Precision, Recall
  - [ ] F1-Score, ROC-AUC
  - [ ] Confusion matrix plotting
- [ ] Run: `python train.py` → trains both models successfully

### Experiment Tracking (5 marks)
- [ ] MLflow integration in `src/models/trainer.py`
- [ ] Logs parameters, metrics, and artifacts
- [ ] Run: `mlflow ui --port 5001` → shows experiments at http://localhost:5001
- [ ] Can compare model runs visually

### Model Packaging (7 marks)
- [ ] Models saved to `models/best_model.pkl`
- [ ] Preprocessor saved to `models/preprocessor.pkl`
- [ ] `requirements.txt` with pinned versions
- [ ] `setup.py` for package installation
- [ ] Fresh environment test:
  ```bash
  python -m venv test_venv
  source test_venv/bin/activate
  pip install -r requirements.txt
  python train.py  # Should work identically
  ```

### Testing & CI/CD (8 marks)
- [ ] `tests/test_data.py` - preprocessing tests pass
- [ ] `tests/test_models.py` - model training tests pass
- [ ] `tests/test_api.py` - API endpoint tests pass
- [ ] Run: `pytest tests/ -v --cov=src` → passes with >85% coverage
- [ ] `.github/workflows/ci_cd.yml` exists with:
  - [ ] Linting jobs (Black, Flake8)
  - [ ] Unit test jobs
  - [ ] Model training job
  - [ ] Docker build job
- [ ] GitHub Actions workflow runs on push/PR

### Docker (5 marks)
- [ ] `Dockerfile` exists
- [ ] Builds: `docker build -t heart-disease-api:latest .` ✓
- [ ] Runs: `docker run -p 5000:5000 heart-disease-api:latest` ✓
- [ ] Health check works: `curl http://localhost:5000/health` → 200
- [ ] Prediction works:
  ```bash
  curl -X POST http://localhost:5000/predict \
    -H "Content-Type: application/json" \
    -d '{"age": 50, "sex": 1, ...}'
  # Returns prediction with confidence
  ```
- [ ] `docker-compose.yml` includes API, MLflow, Prometheus, Grafana

### Kubernetes (7 marks)
- [ ] `deployment/kubernetes/deployment.yaml` exists
- [ ] `deployment/kubernetes/service.yaml` exists
- [ ] `deployment/kubernetes/hpa.yaml` exists
- [ ] Deploy to Minikube:
  ```bash
  minikube start
  kubectl apply -f deployment/kubernetes/
  kubectl get pods  # Shows 3 replicas
  ```
- [ ] Service accessible: `kubectl port-forward svc/heart-disease-api 5000:80`
- [ ] API responds: `curl http://localhost:5000/health`

### Monitoring & Logging (3 marks)
- [ ] `monitoring/prometheus.yml` configured
- [ ] `monitoring/alert_rules.yml` with alert rules
- [ ] API logs requests (check `docker logs`)
- [ ] Docker Compose starts Prometheus: http://localhost:9090
- [ ] Docker Compose starts Grafana: http://localhost:3000
- [ ] Metrics accessible: `curl http://localhost:5000/metrics`

### Documentation (2 marks)
- [ ] `README.md` with quick start
- [ ] `DEPLOYMENT_GUIDE.md` with all deployment options
- [ ] `IMPLEMENTATION_GUIDE.md` with detailed instructions
- [ ] Setup/install instructions clear
- [ ] Code comments on complex logic
- [ ] All markdown files render correctly

## 📊 Generated Outputs

- [ ] EDA visualizations saved in `screenshots/`
  - [ ] Class distribution
  - [ ] Feature distributions
  - [ ] Correlation heatmap
  - [ ] Feature vs target plots
- [ ] Model trained and saved: `models/best_model.pkl`
- [ ] Preprocessor saved: `models/preprocessor.pkl`
- [ ] MLflow experiments visible at http://localhost:5001
- [ ] Tests passing with coverage report
- [ ] CI/CD workflow completed successfully

## 🎥 Media & Reporting

### Final Report (10 pages)
- [ ] Title page with name, date, assignment ID
- [ ] Executive summary (1 page)
- [ ] Problem statement & dataset overview (1 page)
- [ ] EDA findings with visualizations (2 pages)
- [ ] Feature engineering & model selection (1 page)
- [ ] Experiment tracking summary (1 page)
- [ ] Architecture diagram (ASCII or image) (1 page)
- [ ] CI/CD & deployment workflow (1 page)
- [ ] Screenshots of running system (1 page)
- [ ] Performance metrics & conclusions (1 page)

### Screenshots (in `screenshots/` folder)
- [ ] EDA class distribution chart
- [ ] Feature correlation heatmap
- [ ] MLflow experiments comparison UI
- [ ] API prediction response (health check)
- [ ] Docker container running
- [ ] Kubernetes pods running
- [ ] Prometheus metrics page
- [ ] Grafana dashboard
- [ ] GitHub Actions CI/CD pipeline
- [ ] Test coverage report

### Video Recording (5-10 min)
- [ ] Shows complete training pipeline execution
- [ ] Demonstrates API prediction (working model)
- [ ] Shows Kubernetes deployment
- [ ] Shows monitoring dashboards
- [ ] Includes narration/explanations
- [ ] Format: MP4 or WebM
- [ ] Uploaded to GitHub or cloud storage (link provided)

## 🏗️ Code Quality

- [ ] No hardcoded secrets or API keys
- [ ] All imports organized
- [ ] PEP 8 compliance (Black formatted)
- [ ] Docstrings on all functions
- [ ] Type hints where applicable
- [ ] Error handling for edge cases
- [ ] Logging used for debugging
- [ ] No print() statements in production code

## 📁 GitHub Repository

- [ ] Repository created (public or private)
- [ ] All files pushed to main/master branch
- [ ] `.gitignore` prevents data/models/logs upload
- [ ] README visible on repo home page
- [ ] Deployment guide accessible
- [ ] All assets present (code, notebooks, deployment files)
- [ ] Repository link working and accessible

## 🚀 Final Verification

```bash
# Run this in project directory to verify all components:

# 1. Check file structure
ls -la                          # Project files present
ls -la src/                     # Source code present
ls -la tests/                   # Tests present
ls -la deployment/              # Deployment files present

# 2. Verify data download
python data/download_data.py    # Dataset downloads successfully

# 3. Verify training
python train.py                 # Training completes and saves models

# 4. Verify tests
pytest tests/ -v --cov=src      # All tests pass with coverage >85%

# 5. Verify Docker
docker build -t test:latest .   # Image builds successfully
docker run -p 5000:5000 test    # Container starts and API responds

# 6. Verify Kubernetes
minikube start
kubectl apply -f deployment/kubernetes/
kubectl get pods                # Shows 3 running pods

# 7. Verify MLflow
mlflow ui --port 5001           # UI accessible at http://localhost:5001
```

## 📋 Submission Items

Package for submission:
- [ ] GitHub repository link (add to submission form)
- [ ] 10-page final report (PDF/DOCX file)
- [ ] Screenshots folder (ZIP archive)
- [ ] Video recording link (YouTube/Drive/etc.)
- [ ] Any additional notes or customizations

## 🎯 Marks Allocation Summary

```
Task                          Marks  Status
1. Data & EDA                   5    ✅
2. Feature Engineering           8    ✅
3. Experiment Tracking           5    ✅
4. Model Packaging               7    ✅
5. CI/CD & Testing               8    ✅
6. Docker                        5    ✅
7. Kubernetes Deploy             7    ✅
8. Monitoring & Logging          3    ✅
9. Documentation                 2    ✅
                               ────────
TOTAL                           50    ✅
```

## 📞 Before Submitting

- [ ] Verified all 9 tasks are complete
- [ ] Tested on clean machine (fresh venv, etc.)
- [ ] Kubernetes deployment works
- [ ] API responds to predictions
- [ ] Tests pass with coverage report
- [ ] Documentation is clear and complete
- [ ] Video shows working pipeline
- [ ] Report follows academic guidelines
- [ ] Code is original or properly attributed
- [ ] No personal/sensitive data committed

## Notes

- All components must work from a fresh `pip install -r requirements.txt`
- Project must be reproducible on any machine
- Code should follow MLOps best practices
- Documentation should be professional quality
- Personalization encouraged (unique features, models, monitoring)

---

**Status:** Ready for Review  
**Recommended Review Time:** 30 minutes  
**Estimated Full Grade Potential:** 50/50 marks  
