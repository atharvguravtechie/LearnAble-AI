
import pandas as pd
import joblib
import json
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ==========================================
# 1. PROJECT PATHS
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = PROJECT_ROOT / "models"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

MODEL_PATH = MODEL_DIR / "learning_status_model.joblib"

# ==========================================
# 2. LOAD MODEL AND TEST DATA
# ==========================================

print("\nLoading trained model...")

model = joblib.load(MODEL_PATH)

X_test = pd.read_csv(DATA_DIR / "X_test.csv")
y_test = pd.read_csv(DATA_DIR / "y_test.csv")[
    "learning_status"
]

print("Model loaded successfully!")
print("Testing records:", len(X_test))

# ==========================================
# 3. GENERATE PREDICTIONS
# ==========================================

print("\nEvaluating model...")

y_pred = model.predict(X_test)

# ==========================================
# 4. CALCULATE ACCURACY
# ==========================================

accuracy = accuracy_score(y_test, y_pred)

print("\n================================")
print(" LEARNABLE MODEL EVALUATION")
print("================================")

print(f"\nAccuracy: {accuracy * 100:.2f}%")

# ==========================================
# 5. CLASSIFICATION REPORT
# ==========================================

report = classification_report(
    y_test,
    y_pred,
    labels=model.classes_,
    target_names=model.classes_,
    zero_division=0,
    output_dict=True
)

print("\nCLASSIFICATION REPORT:\n")

print(
    classification_report(
        y_test,
        y_pred,
        labels=model.classes_,
        target_names=model.classes_,
        zero_division=0
    )
)

# Save classification report
report_df = pd.DataFrame(report).transpose()

report_df.to_csv(
    OUTPUT_DIR / "classification_report.csv"
)

# ==========================================
# 6. CONFUSION MATRIX
# ==========================================

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=model.classes_
)

print("\nCONFUSION MATRIX:\n")
print(pd.DataFrame(
    cm,
    index=model.classes_,
    columns=model.classes_
))

# ==========================================
# 7. SAVE CONFUSION MATRIX HEATMAP
# ==========================================

plt.figure(figsize=(8, 6))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=model.classes_,
    yticklabels=model.classes_
)

plt.title("LearnAble - Confusion Matrix")
plt.xlabel("Predicted Status")
plt.ylabel("Actual Status")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "confusion_matrix.png",
    dpi=300
)

plt.close()

# ==========================================
# 8. FEATURE IMPORTANCE VISUALIZATION
# ==========================================

importance_df = pd.DataFrame({
    "feature": X_test.columns,
    "importance": model.feature_importances_
})

importance_df = importance_df.sort_values(
    by="importance",
    ascending=True
)

plt.figure(figsize=(9, 6))

sns.barplot(
    data=importance_df,
    x="importance",
    y="feature"
)

plt.title("LearnAble - Feature Importance")
plt.xlabel("Importance")
plt.ylabel("Student Learning Features")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "feature_importance.png",
    dpi=300
)

plt.close()

# ==========================================
# 9. SAVE EVALUATION METRICS
# ==========================================

metrics = {
    "accuracy": round(float(accuracy), 4),
    "training_data_type": "synthetic",
    "test_records": len(X_test),
    "classes": list(model.classes_),
    "classification_report": report
}

with open(
    OUTPUT_DIR / "evaluation_metrics.json",
    "w"
) as file:
    json.dump(metrics, file, indent=4)

# ==========================================
# 10. FINAL RESULTS
# ==========================================

print("\n================================")
print(" EVALUATION COMPLETED")
print("================================")

print(f"Model Accuracy: {accuracy * 100:.2f}%")

print("\nGenerated evaluation files:")

print("1. classification_report.csv")
print("2. confusion_matrix.png")
print("3. feature_importance.png")
print("4. evaluation_metrics.json")

print("\nSaved inside:", OUTPUT_DIR)

print("\nLearnAble model evaluation successful!")
