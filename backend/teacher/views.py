
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from google import genai


class AITeacherAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        # Get question and language from frontend
        question = request.data.get("question", "").strip()
        language = request.data.get("language", "English").strip()

        # Validate question
        if not question:
            return Response(
                {"error": "Please enter a question."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate supported languages
        supported_languages = ["English", "Hindi", "Marathi"]

        if language not in supported_languages:
            language = "English"

        # Check Gemini API key
        if not settings.GEMINI_API_KEY:
            return Response(
                {
                    "success": False,
                    "error": "Gemini API key is not configured on the server."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:

            # Connect to Gemini
            client = genai.Client(
                api_key=settings.GEMINI_API_KEY
            )

            # Structured teaching prompt
            prompt = f"""
You are LearnAble AI, a friendly, patient and professional school teacher.

Your job is to help students understand difficult topics in a simple way.

TEACHING INSTRUCTIONS:

1. Respond only in {language}.
2. Start with a short and clear definition of the topic.
3. Use meaningful headings.
4. Explain the concept step by step.
5. Use bullet points for important information.
6. Include one simple real-life example.
7. Explain important scientific or technical terms.
8. Include formulas when relevant for science and mathematics.
9. For mathematics, explain calculations step by step.
10. Avoid unnecessary greetings and repetition.
11. Keep explanations suitable for school and college students.
12. Be accurate, encouraging and easy to understand.
13. If the question is unclear, politely ask the student to clarify.
14. Do not invent facts.
15. End with a section titled "Key Points to Remember" containing
    two important points.

RESPONSE FORMAT:

Definition:
Explain the topic briefly.

Explanation:
Explain the topic using simple language and headings.

Example:
Give one easy real-life example.

Key Points to Remember:
- Important point 1
- Important point 2

STUDENT'S QUESTION:
{question}
"""

            # Generate AI response
            result = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt
            )

            answer = result.text

            # Check response
            if not answer:
                return Response(
                    {
                        "success": False,
                        "error": "The AI did not return an answer. Please try again."
                    },
                    status=status.HTTP_502_BAD_GATEWAY
                )

            # Send answer to frontend
            return Response(
                {
                    "success": True,
                    "question": question,
                    "answer": answer,
                    "language": language
                },
                status=status.HTTP_200_OK
            )

        except Exception as error:

            print("Gemini API error:", str(error))

            return Response(
                {
                    "success": False,
                    "error": "Unable to generate an answer. Please check the Gemini configuration and try again."
                },
                status=status.HTTP_502_BAD_GATEWAY
            )
