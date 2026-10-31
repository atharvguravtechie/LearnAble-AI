
import pandas as pd
from pathlib import Path


DATA_DIR = Path("data/raw/ednet")


def load_student_data(csv_path):
    """Load one student's EdNet interaction records."""

    df = pd.read_csv(csv_path)

    required = ["timestamp", "question_id", "user_answer"]

    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df = df[required].copy()

    df["timestamp"] = pd.to_numeric(
        df["timestamp"], errors="coerce"
    )

    df = df.dropna(subset=required)

    df["timestamp"] = df["timestamp"].astype("int64")

    df = df.sort_values("timestamp")

    return df


if __name__ == "__main__":
    files = list(DATA_DIR.glob("*.csv"))

    print("CSV files found:", len(files))

    if files:
        df = load_student_data(files[0])
        print("\nFirst student data:")
        print(df.head())
        print("\nShape:", df.shape)
        print("\nColumns:", df.columns.tolist())
    else:
        print("No CSV files found. Add EdNet student interaction CSVs.")
