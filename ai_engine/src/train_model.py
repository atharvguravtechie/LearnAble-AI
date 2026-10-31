
import pickle
import random
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from dkt_model import DKTModel


# ---------------- CONFIGURATION ----------------

DATA_PATH = "data/processed/student_sequences.pkl"
MODEL_PATH = "models/dkt_model.pth"

MAX_HISTORY = 30
BATCH_SIZE = 64
EPOCHS = 8
LEARNING_RATE = 0.001

random.seed(42)
np.random.seed(42)
torch.manual_seed(42)

DEVICE = torch.device("cpu")


# ---------------- LOAD DATA ----------------

print("Loading student sequences...")

with open(DATA_PATH, "rb") as f:
    students = pickle.load(f)

print("Students:", len(students))


# ---------------- QUESTION MAPPING ----------------

all_questions = sorted({
    q
    for student in students
    for q in student["question_ids"]
})

question_to_idx = {
    question: index + 1
    for index, question in enumerate(all_questions)
}

num_questions = len(question_to_idx)

print("Unique questions:", num_questions)


# ---------------- STUDENT SPLIT ----------------

random.shuffle(students)

split = int(len(students) * 0.8)

train_students = students[:split]
val_students = students[split:]

print("Training students:", len(train_students))
print("Validation students:", len(val_students))


# ---------------- DATASET ----------------

class KnowledgeDataset(Dataset):

    def __init__(self, student_data):

        self.samples = []

        for student in student_data:

            questions = [
                question_to_idx[q]
                for q in student["question_ids"]
            ]

            correctness = student["correctness"]

            for i in range(1, len(questions)):

                start = max(0, i - MAX_HISTORY)

                history_q = questions[start:i]
                history_c = correctness[start:i]

                next_q = questions[i]
                target = correctness[i]

                # Left padding to fixed history length
                padding = MAX_HISTORY - len(history_q)

                history_q = [0] * padding + history_q
                history_c = [0] * padding + history_c

                self.samples.append((
                    history_q,
                    history_c,
                    next_q,
                    target
                ))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, index):

        hq, hc, nq, target = self.samples[index]

        return (
            torch.tensor(hq, dtype=torch.long),
            torch.tensor(hc, dtype=torch.float32),
            torch.tensor(nq, dtype=torch.long),
            torch.tensor(target, dtype=torch.float32)
        )


train_dataset = KnowledgeDataset(train_students)
val_dataset = KnowledgeDataset(val_students)

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True
)

val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False
)

print("Training samples:", len(train_dataset))
print("Validation samples:", len(val_dataset))


# ---------------- MODEL ----------------

model = DKTModel(num_questions).to(DEVICE)

criterion = nn.BCEWithLogitsLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=LEARNING_RATE
)


# ---------------- TRAINING ----------------

print("\nStarting LSTM training...\n")

for epoch in range(EPOCHS):

    model.train()

    total_loss = 0

    for history_q, history_c, next_q, target in train_loader:

        history_q = history_q.to(DEVICE)
        history_c = history_c.to(DEVICE)
        next_q = next_q.to(DEVICE)
        target = target.to(DEVICE)

        optimizer.zero_grad()

        predictions = model(
            history_q,
            history_c,
            next_q
        )

        loss = criterion(predictions, target)

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

    average_loss = total_loss / max(len(train_loader), 1)


    # ---------------- VALIDATION ----------------

    model.eval()

    correct = 0
    total = 0

    with torch.no_grad():

        for history_q, history_c, next_q, target in val_loader:

            predictions = model(
                history_q,
                history_c,
                next_q
            )

            probabilities = torch.sigmoid(predictions)

            predicted_labels = (probabilities >= 0.5).float()

            correct += (
                predicted_labels == target
            ).sum().item()

            total += target.numel()

    accuracy = correct / max(total, 1)

    print(
        f"Epoch {epoch + 1}/{EPOCHS} | "
        f"Loss: {average_loss:.4f} | "
        f"Validation Accuracy: {accuracy * 100:.2f}%"
    )


# ---------------- SAVE MODEL ----------------

Path("models").mkdir(exist_ok=True)

torch.save({
    "model_state_dict": model.state_dict(),
    "question_to_idx": question_to_idx,
    "num_questions": num_questions,
    "max_history": MAX_HISTORY,
    "embedding_dim": 32,
    "hidden_dim": 64
}, MODEL_PATH)

print("\nTRAINING COMPLETE")
print("Model saved to:", MODEL_PATH)
