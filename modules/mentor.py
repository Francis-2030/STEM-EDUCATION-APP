# modules/mentor.py
import openai
from config import OPENAI_KEY

class AIMentor:
    def __init__(self):
        openai.api_key = OPENAI_KEY
        self.feedback_history = []
    
    def get_feedback(self, code):
        """Get AI-powered code review"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a Python tutor. Provide constructive feedback."},
                    {"role": "user", "content": f"Review this code:\n{code}"}
                ],
                temperature=0.5,
                max_tokens=200
            )
            feedback = response.choices[0].message.content
            self.feedback_history.append((code, feedback))
            return feedback
        except Exception as e:
            return f"AI service error: {str(e)}"