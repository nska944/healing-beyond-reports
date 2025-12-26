import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = None
if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)


def analyze_medical_report(text):
    if not client:
        return (
            "AI analysis service is temporarily unavailable.\n\n"
            "This deployment is running in demo mode without external AI access.\n"
            "The system architecture supports AI-assisted diagnosis using NLP "
            "and can be enabled by configuring the API key."
        )

    prompt = f"""
You are an AI medical assistant.

Analyze the following medical report text and provide:
- Overall health summary
- Possible risk indicators
- Lifestyle recommendations
- When to consult a doctor

Medical Report:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content
