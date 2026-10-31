
import pickle

from student_growth import StudentGrowthAnalyzer


with open("data/processed/student_sequences.pkl", "rb") as f:
    students = pickle.load(f)

analyzer = StudentGrowthAnalyzer()

student = students[0]

questions = student["question_ids"]
correctness = student["correctness"]

print("\n========== REAL STUDENT TEST ==========")

print("Student ID:", student["student_id"])
print("Total interactions:", len(questions))

print("\nGROWTH ANALYSIS")
print(analyzer.analyze_growth(correctness))

if len(questions) >= 2:

    probability = analyzer.predict_next_performance(
        questions[:-1],
        correctness[:-1],
        questions[-1]
    )

    print("\nLAST QUESTION PREDICTION")
    print("Question:", questions[-1])
    print("Actual result:", correctness[-1])
    print("Predicted correctness probability:", probability)

print("\n=======================================")
