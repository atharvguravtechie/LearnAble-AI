
import sys

from pathlib import Path

# Ensure project root is available for imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.predictor import predict_learning_gap


# ==========================================
# 1. STUDENT TEST SCENARIOS
# ==========================================

test_students = {

    "Weak Student": {
        "quiz_attempts": 2,
        "average_score": 38,
        "incorrect_percentage": 62,
        "days_since_revision": 25,
        "score_consistency": 20,
        "topic_difficulty": 4
    },

    "Developing Student": {
        "quiz_attempts": 3,
        "average_score": 65,
        "incorrect_percentage": 35,
        "days_since_revision": 7,
        "score_consistency": 10,
        "topic_difficulty": 3
    },

    "Strong Student": {
        "quiz_attempts": 6,
        "average_score": 92,
        "incorrect_percentage": 8,
        "days_since_revision": 1,
        "score_consistency": 3,
        "topic_difficulty": 2
    }
}


# ==========================================
# 2. TEST ALL THREE SCENARIOS
# ==========================================

print("\n====================================")
print(" LEARNABLE - STUDENT SCENARIO TESTS")
print("====================================")

for student_name, student_data in test_students.items():

    result = predict_learning_gap(student_data)

    print(f"\nStudent: {student_name}")
    print("-" * 40)

    print("Predicted status:", result["learning_status"])

    print("Confidence:", result["confidence"], "%")

    print(
        "Recommendation:",
        result["recommendation"]["title"]
    )

    print(
        "Action:",
        result["recommendation"]["action"]
    )

    print("Probabilities:", result["class_probabilities"])

    # Basic output validation
    assert result["success"] is True

    assert result["learning_status"] in [
        "weak", "developing", "strong"
    ]

    assert 0 <= result["confidence"] <= 100

    assert result["recommendation"]["action"] in [
        "revise_topic",
        "practice_questions",
        "move_to_next_topic"
    ]

    assert abs(
        sum(result["class_probabilities"].values()) - 100
    ) < 0.1


# ==========================================
# 3. TEST INVALID INPUT
# ==========================================

print("\n====================================")
print(" INVALID INPUT TEST")
print("====================================")

try:

    invalid_student = {
        "quiz_attempts": 2,
        "average_score": 150,
        "incorrect_percentage": 62,
        "days_since_revision": 25,
        "score_consistency": 20,
        "topic_difficulty": 4
    }

    predict_learning_gap(invalid_student)

except ValueError as error:

    print("Invalid input correctly rejected!")
    print("Error:", error)

else:

    raise AssertionError("Invalid input was not rejected!")


# ==========================================
# 4. FINAL RESULT
# ==========================================

print("\n====================================")
print(" ALL PREDICTION TESTS COMPLETED")
print("====================================")
