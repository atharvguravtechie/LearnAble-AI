
import torch
import numpy as np

from dkt_model import DKTModel


MODEL_PATH = "models/dkt_model.pth"


class StudentGrowthAnalyzer:

    def __init__(self):

        self.device = torch.device("cpu")

        checkpoint = torch.load(
            MODEL_PATH,
            map_location=self.device,
            weights_only=False
        )

        self.question_to_idx = checkpoint["question_to_idx"]
        self.max_history = checkpoint["max_history"]

        self.model = DKTModel(
            num_questions=checkpoint["num_questions"],
            embedding_dim=checkpoint["embedding_dim"],
            hidden_dim=checkpoint["hidden_dim"]
        )

        self.model.load_state_dict(
            checkpoint["model_state_dict"]
        )

        self.model.eval()

    def predict_next_performance(
        self,
        question_ids,
        correctness,
        next_question_id
    ):

        if next_question_id not in self.question_to_idx:
            return None

        history = []

        for q in question_ids[-self.max_history:]:

            if q not in self.question_to_idx:
                return None

            history.append(self.question_to_idx[q])

        results = correctness[-self.max_history:]

        padding = self.max_history - len(history)

        history = [0] * padding + history
        results = [0] * padding + results

        next_q = self.question_to_idx[next_question_id]

        with torch.no_grad():

            logits = self.model(
                torch.tensor([history], dtype=torch.long),
                torch.tensor([results], dtype=torch.float32),
                torch.tensor([next_q], dtype=torch.long)
            )

            probability = torch.sigmoid(logits).item()

        return round(probability * 100, 2)

    def analyze_growth(self, correctness):

        if len(correctness) < 4:
            return {
                "status": "insufficient_data",
                "message": "More learning interactions are needed."
            }

        midpoint = len(correctness) // 2

        early = np.mean(correctness[:midpoint]) * 100
        recent = np.mean(correctness[midpoint:]) * 100

        growth = recent - early

        if growth >= 10:
            level = "Improving"
        elif growth <= -10:
            level = "Declining"
        else:
            level = "Stable"

        return {
            "early_accuracy": round(early, 2),
            "recent_accuracy": round(recent, 2),
            "growth_percentage_points": round(growth, 2),
            "status": level
        }


if __name__ == "__main__":

    analyzer = StudentGrowthAnalyzer()

    sample = [0, 1, 0, 1, 1, 1, 0, 1, 1, 1]

    print("\nSTUDENT GROWTH ANALYSIS")
    print(analyzer.analyze_growth(sample))

    probability = analyzer.predict_next_performance(
        ["q5643", "q6008", "q6168", "q219"],
        [0, 0, 1, 1],
        "q4227"
    )

    print("\nNEXT QUESTION PREDICTION")
    print("Predicted correctness probability:", probability)
