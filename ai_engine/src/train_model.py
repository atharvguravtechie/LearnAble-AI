
import pandas as pd
import joblib

from pathlib import Path
from sklearn.ensemble import RandomForestClassifier

# ==========================================
# 1. PROJECT PATHS
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = PROJECT_ROOT / "models"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# 2. LOAD TRAINING DATA
# ==========================================

print("\nLoading training dataset...")

X_train = pd.read_csv(DATA_DIR / "X_train.csv")
y_train = pd.read_csv(DATA_DIR / "y_train.csv")[
    "learning_status"
]

print("Training features:", X_train.shape)
print("Training labels:", y_train.shape)

# ==========================================
# 3. DEFINE RANDOM FOREST
# ==========================================

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    min_samples_split=4,
    min_samples_leaf=2,
    max_features="sqrt",
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

# ==========================================
# 4. TRAIN THE MODEL
# ==========================================

print("\nTraining Random Forest Classifier...")
print("Please wait...\n")

model.fit(X_train, y_train)

print("MODEL TRAINING COMPLETED!")

# ==========================================
# 5. DISPLAY MODEL INFORMATION
# ==========================================

print("\nModel configuration:")
print("Algorithm: Random Forest Classifier")
print("Number of trees:", model.n_estimators)
print("Maximum depth:", model.max_depth)
print("Features:", list(X_train.columns))
print("Classes:", list(model.classes_))

# ==========================================
# 6. FEATURE IMPORTANCE
# ==========================================

importance_df = pd.DataFrame({
    "feature": X_train.columns,
    "importance": model.feature_importances_
})

importance_df = importance_df.sort_values(
    by="importance",
    ascending=False
)

print("\nFEATURE IMPORTANCE:")
print(importance_df.to_string(index=False))

importance_df.to_csv(
    OUTPUT_DIR / "feature_importance.csv",
    index=False
)

# ==========================================
# 7. SAVE TRAINED MODEL
# ==========================================

model_path = MODEL_DIR / "learning_status_model.joblib"

joblib.dump(model, model_path)

print("\n==========================================")
print(" LEARNABLE AI MODEL SAVED SUCCESSFULLY")
print("==========================================")

print("Model location:")
print(model_path)

print("\nReady for evaluation and prediction!")
