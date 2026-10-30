
import joblib
import pandas as pd
from src.recommendations import generate_recommendation
from pathlib import Path

# ==========================================
# 1. MODEL CONFIGURATION
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "learning_status_model.joblib"
)

FEATURES = [
    "quiz_attempts",
    "average_score",
    "incorrect_percentage",
    "days_since_revision",
    "score_consistency",
    "topic_difficulty"
]

VALID_STATUSES = {"weak", "developing", "strong"}


# ==========================================
# 2. LOAD TRAINED MODEL
# ==========================================

def load_model():

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Trained model not found: {MODEL_PATH}"
        )

    model = joblib.load(MODEL_PATH)

    if not hasattr(model, "predict_proba"):
        raise TypeError(
            "Loaded model does not support probabilities."
        )

    return model


model = load_model()


# ==========================================
# 3. INPUT VALIDATION
# ==========================================

def validate_student_data(student_data):

    if not isinstance(student_data, dict):
        raise TypeError(
            "student_data must be a dictionary."
        )

    missing_features = [
        feature
        for feature in FEATURES
        if feature not in student_data
    ]

    if missing_features:
        raise ValueError(
            f"Missing features: {missing_features}"
        )

    clean_data = {}

    for feature in FEATURES:

        value = student_data[feature]

        if isinstance(value, bool):
            raise ValueError(
                f"{feature} must be numeric."
            )

        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError(
                f"{feature} must be numeric."
            )

        if not pd.notna(value) or value in (float("inf"), float("-inf")):
            raise ValueError(
                f"{feature} must be a finite number."
            )

        clean_data[feature] = value

    # Feature-specific validation

    if clean_data["quiz_attempts"] < 1:
        raise ValueError("quiz_attempts must be >= 1.")

    if not 0 <= clean_data["average_score"] <= 100:
        raise ValueError("average_score must be 0-100.")

    if not 0 <= clean_data["incorrect_percentage"] <= 100:
        raise ValueError(
            "incorrect_percentage must be 0-100."
        )

    if clean_data["days_since_revision"] < 0:
        raise ValueError(
            "days_since_revision cannot be negative."
        )

    if not 1 <= clean_data["score_consistency"] <= 35:
        raise ValueError(
            "score_consistency must be between 1 and 35."
        )

    difficulty = clean_data["topic_difficulty"]

    if difficulty not in [1, 2, 3, 4, 5]:
        raise ValueError(
            "topic_difficulty must be an integer from 1 to 5."
        )

    return clean_data


# ==========================================
# 4. RECOMMENDATION ENGINE
# ==========================================




# ==========================================
# 5. MAIN PREDICTION FUNCTION
# ==========================================

def predict_learning_gap(student_data):

    # Validate incoming student data
    clean_data = validate_student_data(student_data)

    # Convert dictionary into model input
    input_df = pd.DataFrame(
        [clean_data],
        columns=FEATURES
    )

    # Machine learning prediction
    predicted_status = model.predict(input_df)[0]

    # Prediction probabilities
    probabilities = model.predict_proba(input_df)[0]

    class_probabilities = {
        str(label): round(float(probability) * 100, 2)
        for label, probability in zip(
            model.classes_,
            probabilities
        )
    }

    # Confidence of predicted class
    confidence = max(probabilities) * 100

    # Separate recommendation logic
    recommendation = generate_recommendation(
        predicted_status
    )

    # Structured output
    result = {
        "success": True,

        "learning_status": str(predicted_status),

        "confidence": round(float(confidence), 2),

        "class_probabilities": class_probabilities,

        "recommendation": recommendation,

        "model": "LearnAble Random Forest Classifier"
    }

    return result


# ==========================================
# 6. BASIC EXECUTION TEST
# ==========================================

if __name__ == "__main__":

    test_student = {
        "quiz_attempts": 2,
        "average_score": 38,
        "incorrect_percentage": 62,
        "days_since_revision": 25,
        "score_consistency": 20,
        "topic_difficulty": 4
    }

    result = predict_learning_gap(test_student)

    print("\n================================")
    print(" LEARNABLE AI PREDICTION")
    print("================================")

    for key, value in result.items():
        print(f"\n{key}: {value}")

    print("\nPrediction completed successfully!")
