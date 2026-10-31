
import zipfile
import pandas as pd
import random
import pickle
from pathlib import Path
from io import BytesIO

ZIP_PATH = "data/raw/ednet/EdNet-KT1.zip"
META_PATH = "data/raw/ednet/questions.parquet"
OUTPUT_PATH = "data/processed/student_sequences.pkl"

MAX_STUDENTS = 1000
MAX_INTERACTIONS = 100
MIN_INTERACTIONS = 5

def build_sequences():

    print("Loading question metadata...")

    metadata = pd.read_parquet(META_PATH)

    metadata["question_id"] = metadata["question_id"].astype(str)

    answer_map = dict(zip(
        metadata["question_id"],
        metadata["correct_answer"].astype(str).str.strip().str.lower()
    ))

    print("Questions loaded:", len(answer_map))

    print("Opening EdNet ZIP...")

    sequences = []

    with zipfile.ZipFile(ZIP_PATH, "r") as archive:

        student_files = [
            name for name in archive.namelist()
            if name.startswith("KT1/u") and name.endswith(".csv")
        ]

        random.seed(42)
        random.shuffle(student_files)

        selected = student_files[:MAX_STUDENTS]

        print("Selected students:", len(selected))

        for index, filename in enumerate(selected):

            try:
                with archive.open(filename) as file:
                    df = pd.read_csv(BytesIO(file.read()))

                required = [
                    "timestamp",
                    "question_id",
                    "user_answer"
                ]

                if not all(col in df.columns for col in required):
                    continue

                df["question_id"] = df["question_id"].astype(str)
                df["user_answer"] = (
                    df["user_answer"].astype(str).str.strip().str.lower()
                )

                df["correct_answer"] = df["question_id"].map(answer_map)

                df = df.dropna(
                    subset=["correct_answer", "timestamp"]
                )

                df["timestamp"] = pd.to_numeric(
                    df["timestamp"], errors="coerce"
                )

                df = df.dropna(subset=["timestamp"])
                df = df.sort_values("timestamp")

                df["correctness"] = (
                    df["user_answer"] == df["correct_answer"]
                ).astype(int)

                df = df.drop_duplicates(
                    subset=["solving_id"]
                ) if "solving_id" in df.columns else df

                df = df.tail(MAX_INTERACTIONS)

                if len(df) < MIN_INTERACTIONS:
                    continue

                sequences.append({
                    "student_id": filename.split("/")[-1].replace(".csv", ""),
                    "question_ids": df["question_id"].tolist(),
                    "correctness": df["correctness"].tolist()
                })

            except Exception as error:
                print("Skipped:", filename, error)

            if (index + 1) % 100 == 0:
                print(
                    "Processed:", index + 1,
                    "| Valid students:", len(sequences)
                )

    Path(OUTPUT_PATH).parent.mkdir(
        parents=True, exist_ok=True
    )

    with open(OUTPUT_PATH, "wb") as file:
        pickle.dump(sequences, file)

    print("\nDATASET CREATED")
    print("Valid students:", len(sequences))
    print("Saved to:", OUTPUT_PATH)

    if sequences:
        print("Example sequence:")
        print(sequences[0])

if __name__ == "__main__":
    build_sequences()
