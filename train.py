#!/usr/bin/env python
"""
Complete MLOps training pipeline with MLflow tracking.

Executes:
1. Data loading & preprocessing
2. Train-test split
3. Model training (Logistic Regression & Random Forest)
4. Hyperparameter tuning
5. Evaluation & logging with MLflow
6. Model packaging
"""
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.data.loader import load_data, train_test_split_data
from src.data.preprocessor import HeartDiseasePreprocessor, handle_missing_values
from src.models.trainer import ModelTrainer
from src.models.evaluator import ModelEvaluator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Run complete training pipeline."""

    logger.info("="*80)
    logger.info("MLOps Training Pipeline - Heart Disease Prediction")
    logger.info("="*80)

    # Paths
    data_path = Path("data/heart.csv")
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)

    # ==================== Data Loading ====================
    logger.info("\n[1/6] Loading and preprocessing data...")

    if not data_path.exists():
        logger.error(f"Dataset not found at {data_path}")
        logger.info("Run: python data/download_data.py")
        return False

    df = load_data(str(data_path))
    logger.info(f"✓ Loaded dataset: {df.shape}")

    # Handle missing values
    df = handle_missing_values(df, strategy='mean')
    logger.info(f"✓ Handled missing values")

    # ==================== Train-Test Split ====================
    logger.info("\n[2/6] Splitting data...")

    X_train, X_test, y_train, y_test = train_test_split_data(df, test_size=0.2)
    logger.info(f"✓ Train set: {X_train.shape}, Test set: {X_test.shape}")

    # ==================== Preprocessing ====================
    logger.info("\n[3/6] Preprocessing features...")

    preprocessor = HeartDiseasePreprocessor()
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    logger.info(f"✓ Features scaled: {X_train_processed.shape}")

    # Save preprocessor
    preprocessor_path = models_dir / "preprocessor.pkl"
    preprocessor.save(str(preprocessor_path))
    logger.info(f"✓ Preprocessor saved: {preprocessor_path}")

    # ==================== Model Training ====================
    logger.info("\n[4/6] Training models...")

    trainer = ModelTrainer(experiment_name="heart_disease_production")

    # Train Logistic Regression
    logger.info("  - Training Logistic Regression...")
    lr_model, lr_metrics = trainer.train_logistic_regression(
        X_train_processed, y_train, X_test_processed, y_test
    )
    logger.info(f"  ✓ LR Accuracy: {lr_metrics['accuracy']:.4f}, ROC-AUC: {lr_metrics['roc_auc']:.4f}")

    # Train Random Forest
    logger.info("  - Training Random Forest...")
    rf_model, rf_metrics = trainer.train_random_forest(
        X_train_processed, y_train, X_test_processed, y_test
    )
    logger.info(f"  ✓ RF Accuracy: {rf_metrics['accuracy']:.4f}, ROC-AUC: {rf_metrics['roc_auc']:.4f}")

    # ==================== Hyperparameter Tuning ====================
    logger.info("\n[5/6] Hyperparameter tuning...")

    logger.info("  - Tuning Random Forest...")
    best_model, best_params, best_score = trainer.hyperparameter_tuning(
        X_train_processed, y_train, model_type='random_forest'
    )
    logger.info(f"  ✓ Best CV Score: {best_score:.4f}")
    logger.info(f"  ✓ Best params: {best_params}")

    # ==================== Model Packaging ====================
    logger.info("\n[6/6] Saving best model...")

    best_model_path = models_dir / "best_model.pkl"
    trainer.save_model(best_model, str(best_model_path))
    logger.info(f"✓ Best model saved: {best_model_path}")

    # ==================== Summary ====================
    logger.info("\n" + "="*80)
    logger.info("Training Pipeline Completed Successfully!")
    logger.info("="*80)
    logger.info("\nModel Artifacts:")
    logger.info(f"  - Best Model: {best_model_path}")
    logger.info(f"  - Preprocessor: {preprocessor_path}")
    logger.info(f"\nModel Performance:")
    logger.info(f"  - Logistic Regression ROC-AUC: {lr_metrics['roc_auc']:.4f}")
    logger.info(f"  - Random Forest ROC-AUC: {rf_metrics['roc_auc']:.4f}")
    logger.info(f"  - Tuned Random Forest CV Score: {best_score:.4f}")
    logger.info("\nNext steps:")
    logger.info("  1. Review experiments: mlflow ui --port 5001")
    logger.info("  2. Run tests: pytest tests/ -v")
    logger.info("  3. Deploy API: docker-compose up -d")
    logger.info("  4. Test API: curl http://localhost:5000/health")

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
