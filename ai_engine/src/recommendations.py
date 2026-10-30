def generate_recommendation(status):
    """
    Generate a learning recommendation based on predicted status.

    This is rule-based logic, separate from the ML classifier.
    """

    recommendations = {
        "weak": {
            "action": "revise_topic",
            "title": "Focused Revision",
            "explanation": (
                "Your performance indicates learning gaps. "
                "Revise the topic and review its key concepts "
                "before attempting another quiz."
            )
        },

        "developing": {
            "action": "practice_questions",
            "title": "More Practice",
            "explanation": (
                "You are making progress, but need more practice. "
                "Attempt additional questions and take another quiz "
                "to strengthen your understanding."
            )
        },

        "strong": {
            "action": "move_to_next_topic",
            "title": "Advance to Next Topic",
            "explanation": (
                "You have demonstrated strong performance. "
                "You can move forward to the next topic."
            )
        }
    }

    if status not in recommendations:
        raise ValueError(f"Unknown learning status: {status}")

    return recommendations[status]