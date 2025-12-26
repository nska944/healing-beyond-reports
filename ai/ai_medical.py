import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_medical_report(text):
    prompt = f"""
You are an AI clinical assistant helping patients understand their medical reports.

Your task:
- Write in clear, calm, professional language.
- Do surface level diagnose diseases.
- Do NOT prescribe medicines.
- Explain findings in a patient-friendly way.
- Highlight general health patterns if visible.
- Suggest basic lifestyle improvements if relevant.
- Encourage consulting a qualified doctor for medical decisions.

Structure the response exactly like this:

1. Overall Summary
2. Key Observations (if any)
3. General Wellness Suggestions
4. Important Note

Medical Report Text:
{text[:2500]}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        return response.choices[0].message.content

    except Exception as e:
        return (
            "AI summary could not be generated at this time.\n\n"
            "Please consult a healthcare professional for interpretation."
        )
