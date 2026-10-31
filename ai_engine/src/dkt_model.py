
import torch
import torch.nn as nn


class DKTModel(nn.Module):
    def __init__(
        self,
        num_questions,
        embedding_dim=32,
        hidden_dim=64
    ):
        super().__init__()

        self.question_embedding = nn.Embedding(
            num_questions + 1,
            embedding_dim,
            padding_idx=0
        )

        self.lstm = nn.LSTM(
            input_size=embedding_dim + 1,
            hidden_size=hidden_dim,
            batch_first=True
        )

        self.output = nn.Linear(
            hidden_dim + embedding_dim,
            1
        )

    def forward(self, history_questions, history_correct, next_question):

        # Embed questions in the student's learning history
        question_emb = self.question_embedding(history_questions)

        # Add correctness information to each interaction
        correctness = history_correct.unsqueeze(-1).float()

        # Combine question and correctness features
        history = torch.cat(
            [question_emb, correctness],
            dim=-1
        )

        # Learn sequential patterns
        _, (hidden, _) = self.lstm(history)

        student_state = hidden[-1]

        # Embed the question we want to predict
        next_question_emb = self.question_embedding(next_question)

        # Combine student knowledge state and next question
        combined = torch.cat(
            [student_state, next_question_emb],
            dim=1
        )

        logits = self.output(combined).squeeze(1)

        return logits
