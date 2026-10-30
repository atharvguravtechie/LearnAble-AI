
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

# -----------------------------------
# 1. PROJECT PATHS
# -----------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "learning_data.csv"

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------
# 2. LOAD DATASET
# -----------------------------------

print("\nLoading LearnAble dataset...")

df = pd.read_csv(DATA_PATH)

print("Dataset loaded:", df.shape)

# -----------------------------------
# 3. VERIFY REQUIRED COLUMNS
# -----------------------------------

FEATURES = [
    "quiz_attempts",
    "average_score",
    "incorrect_percentage",
    "days_since_revision",
    "score_consistency",
    "topic_difficulty"
]

TARGET = "learning_status"

required_columns = FEATURES + [TARGET]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns: {missing_columns}"
    )

df = df[required_columns].copy()

# -----------------------------------
# 4. DATA INSPECTION
# -----------------------------------

print("\n--- Dataset Information ---")
print(df.info())

print("\n--- Missing Values ---")
print(df.isnull().sum())

if df.isnull().any().any():
    raise ValueError("Dataset contains missing values!")

print("\n--- Duplicate Records ---")
print("Duplicates:", df.duplicated().sum())

print("\n--- Statistical Summary ---")
print(df.describe())

# -----------------------------------
# 5. VALIDATE FEATURE RANGES
# -----------------------------------

if not df["average_score"].between(0, 100).all():
    raise ValueError("Invalid average scores!")

if not df["incorrect_percentage"].between(0, 100).all():
    raise ValueError("Invalid incorrect percentages!")

if not df["topic_difficulty"].between(1, 5).all():
    raise ValueError("Invalid topic difficulty!")

if not df["quiz_attempts"].ge(1).all():
    raise ValueError("Invalid quiz attempts!")

if not df["days_since_revision"].ge(0).all():
    raise ValueError("Invalid revision days!")

if not df["score_consistency"].between(1, 35).all():
    raise ValueError("Invalid score consistency!")

# -----------------------------------
# 6. SEPARATE FEATURES AND TARGET
# -----------------------------------

X = df[FEATURES]
y = df[TARGET]

print("\nFeature shape:", X.shape)
print("Target shape:", y.shape)

print("\nTarget distribution:")
print(y.value_counts())

# -----------------------------------
# 7. TRAIN / TEST SPLIT
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# -----------------------------------
# 8. SAVE PROCESSED DATA
# -----------------------------------

X_train.to_csv(PROCESSED_DIR / "X_train.csv", index=False)
X_test.to_csv(PROCESSED_DIR / "X_test.csv", index=False)

y_train.to_frame().to_csv(
    PROCESSED_DIR / "y_train.csv", index=False
)

y_test.to_frame().to_csv(
    PROCESSED_DIR / "y_test.csv", index=False
)

# -----------------------------------
# 9. DISPLAY RESULTS
# -----------------------------------

print("\n================================")
print(" DATA PREPARATION COMPLETED")
print("================================")

print("Training records:", len(X_train))
print("Testing records:", len(X_test))

print("\nTraining class distribution:")
print(y_train.value_counts(normalize=True).round(3))

print("\nTesting class distribution:")
print(y_test.value_counts(normalize=True).round(3))

print("\nSaved files:")
print("X_train.csv")
print("X_test.csv")
print("y_train.csv")
print("y_test.csv")

print("\nAll files saved inside:", PROCESSED_DIR)
