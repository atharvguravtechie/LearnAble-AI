
import numpy as np  # type: ignore[reportMissingImports]
import pandas as pd  # type: ignore[reportMissingModuleSource]
from pathlib import Path

# -----------------------------------
# 1. CONFIGURATION
# -----------------------------------

RANDOM_SEED = 42
NUMBER_OF_RECORDS = 2000

rng = np.random.default_rng(RANDOM_SEED)

# -----------------------------------
# 2. GENERATE STUDENT TOPIC FEATURES
# -----------------------------------

# Hidden student ability (used only to
# simulate realistic student performance)
student_ability = rng.beta(2.4, 1.8, NUMBER_OF_RECORDS)

quiz_attempts = rng.integers(1, 9, NUMBER_OF_RECORDS)

topic_difficulty = rng.integers(1, 6, NUMBER_OF_RECORDS)

days_since_revision = rng.integers(0, 46, NUMBER_OF_RECORDS)

# Practice improves performance
practice_boost = np.minimum(quiz_attempts - 1, 6) * 1.8

# Longer revision gaps can reduce retention
forgetting_penalty = days_since_revision * 0.35

# More difficult topics can reduce raw quiz scores
difficulty_penalty = (topic_difficulty - 1) * 3.5

# Generate average quiz score
average_score = (
    24
    + student_ability * 72
    + practice_boost
    - forgetting_penalty
    - difficulty_penalty
    + rng.normal(0, 9, NUMBER_OF_RECORDS)
)

average_score = np.clip(average_score, 0, 100)

# Incorrect answer percentage
incorrect_percentage = (
    100 - average_score
    + rng.normal(0, 5, NUMBER_OF_RECORDS)
)

incorrect_percentage = np.clip(
    incorrect_percentage, 0, 100
)

# Score consistency:
# Lower standard deviation means more consistent scores.
score_consistency = (
    18
    - student_ability * 10
    + topic_difficulty * 0.7
    + rng.normal(0, 4.5, NUMBER_OF_RECORDS)
)

score_consistency = np.clip(
    score_consistency, 1, 35
)

# -----------------------------------
# 3. GENERATE SYNTHETIC LABELS
# -----------------------------------

# These intermediate scores are used only
# to create synthetic training labels.

recency_score = 100 * np.exp(
    -days_since_revision / 30
)

consistency_score = np.clip(
    100 - score_consistency * 2.5, 0, 100
)

practice_score = (
    np.minimum(quiz_attempts, 6) / 6
) * 100

mastery_score = (
    0.58 * average_score
    + 0.17 * (100 - incorrect_percentage)
    + 0.10 * recency_score
    + 0.08 * consistency_score
    + 0.07 * practice_score
)

# Add noise to avoid perfectly deterministic labels
mastery_score += rng.normal(0, 5, NUMBER_OF_RECORDS)

def assign_learning_status(score):
    if score < 45:
        return "weak"
    elif score < 70:
        return "developing"
    else:
        return "strong"

learning_status = [
    assign_learning_status(score)
    for score in mastery_score
]

# -----------------------------------
# 4. CREATE DATAFRAME
# -----------------------------------

df = pd.DataFrame({
    "quiz_attempts": quiz_attempts,
    "average_score": np.round(average_score, 2),
    "incorrect_percentage": np.round(
        incorrect_percentage, 2
    ),
    "days_since_revision": days_since_revision,
    "score_consistency": np.round(
        score_consistency, 2
    ),
    "topic_difficulty": topic_difficulty,
    "learning_status": learning_status
})

# -----------------------------------
# 5. SAVE DATASET
# -----------------------------------

project_root = Path(__file__).resolve().parent.parent
data_folder = project_root / "data"

data_folder.mkdir(parents=True, exist_ok=True)

output_path = data_folder / "learning_data.csv"

df.to_csv(output_path, index=False)

# -----------------------------------
# 6. DISPLAY RESULTS
# -----------------------------------

print("\n================================")
print(" LEARNABLE SYNTHETIC DATASET")
print("================================")

print("\nDataset shape:", df.shape)

print("\nFirst 5 records:")
print(df.head())

print("\nLearning status distribution:")
print(df["learning_status"].value_counts())

print("\nPercentage distribution:")
print(
    df["learning_status"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDataset saved successfully!")
print(output_path)
