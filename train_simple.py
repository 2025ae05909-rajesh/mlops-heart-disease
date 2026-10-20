#!/usr/bin/env python
"""
Simplified training pipeline (without MLflow for now)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.data.loader import load_data, train_test_split_data
from src.data.preprocessor import HeartDiseasePreprocessor, handle_missing_values
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import joblib

print("="*80)
print("MLOps Training Pipeline - Heart Disease Prediction")
print("="*80)

# Paths
data_path = Path("data/heart.csv")
models_dir = Path("models")
models_dir.mkdir(exist_ok=True)

# Step 1: Load data
print("\n[1/5] Loading and preprocessing data...")
if not data_path.exists():
    print(f"❌ Dataset not found. Run: python data/download_data.py")
    sys.exit(1)

df = load_data(str(data_path))
print(f"[OK] Loaded dataset: {df.shape}")

df = handle_missing_values(df, strategy='mean')
print(f"[OK] Handled missing values")

# Step 2: Train-test split
print("\n[2/5] Splitting data...")
X_train, X_test, y_train, y_test = train_test_split_data(df, test_size=0.2)
print(f"[OK] Train: {X_train.shape}, Test: {X_test.shape}")

# Step 3: Preprocessing
print("\n[3/5] Preprocessing features...")
preprocessor = HeartDiseasePreprocessor()
X_train_scaled = preprocessor.fit_transform(X_train)
X_test_scaled = preprocessor.transform(X_test)
print(f"[OK] Features scaled: {X_train_scaled.shape}")

# Save preprocessor
preprocessor_path = models_dir / "preprocessor.pkl"
preprocessor.save(str(preprocessor_path))
print(f"[OK] Preprocessor saved")

# Step 4: Train models
print("\n[4/5] Training models...")

# Logistic Regression
print("  Training Logistic Regression...")
lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train_scaled, y_train)
y_pred_lr = lr.predict(X_test_scaled)
y_pred_proba_lr = lr.predict_proba(X_test_scaled)[:, 1]

lr_metrics = {
    'accuracy': accuracy_score(y_test, y_pred_lr),
    'precision': precision_score(y_test, y_pred_lr),
    'recall': recall_score(y_test, y_pred_lr),
    'f1': f1_score(y_test, y_pred_lr),
    'roc_auc': roc_auc_score(y_test, y_pred_proba_lr)
}
print(f"  [OK] LR Accuracy: {lr_metrics['accuracy']:.4f}, ROC-AUC: {lr_metrics['roc_auc']:.4f}")

# Random Forest
print("  Training Random Forest...")
rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
rf.fit(X_train_scaled, y_train)
y_pred_rf = rf.predict(X_test_scaled)
y_pred_proba_rf = rf.predict_proba(X_test_scaled)[:, 1]

rf_metrics = {
    'accuracy': accuracy_score(y_test, y_pred_rf),
    'precision': precision_score(y_test, y_pred_rf),
    'recall': recall_score(y_test, y_pred_rf),
    'f1': f1_score(y_test, y_pred_rf),
    'roc_auc': roc_auc_score(y_test, y_pred_proba_rf)
}
print(f"  [OK] RF Accuracy: {rf_metrics['accuracy']:.4f}, ROC-AUC: {rf_metrics['roc_auc']:.4f}")

# Step 5: Save best model
print("\n[5/5] Saving models...")
best_model = rf if rf_metrics['roc_auc'] > lr_metrics['roc_auc'] else lr
best_name = "Random Forest" if rf_metrics['roc_auc'] > lr_metrics['roc_auc'] else "Logistic Regression"

model_path = models_dir / "best_model.pkl"
joblib.dump(best_model, model_path)
print(f"[OK] Best model saved: {model_path}")

lr_path = models_dir / "logistic_regression.pkl"
joblib.dump(lr, lr_path)
print(f"[OK] Logistic Regression saved")

rf_path = models_dir / "random_forest.pkl"
joblib.dump(rf, rf_path)
print(f"[OK] Random Forest saved")

# Summary
print("\n" + "="*80)
print("Training Complete!")
print("="*80)
print(f"\n[OK] Best Model: {best_name}")
print(f"\nLogistic Regression Metrics:")
for k, v in lr_metrics.items():
    print(f"  {k}: {v:.4f}")

print(f"\nRandom Forest Metrics:")
for k, v in rf_metrics.items():
    print(f"  {k}: {v:.4f}")

print(f"\nModel Artifacts:")
print(f"  - Best model: {model_path}")
print(f"  - LR model: {lr_path}")
print(f"  - RF model: {rf_path}")
print(f"  - Preprocessor: {preprocessor_path}")

print(f"\n[OK] Ready for deployment!")
