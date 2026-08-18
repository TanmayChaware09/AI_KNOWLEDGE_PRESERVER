import os
import json
from unittest import result
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def analyze_meeting(transcript, meeting):

    participants = ", ".join(
        [p["name"] for p in meeting["participants"]]
    )

    prompt = f"""
You are an Enterprise AI Knowledge Extraction System.

Your task is to analyze the meeting transcript.

Meeting Title:
{meeting["title"]}

Manager:
{meeting["manager"]}

Participants:
{participants}

Transcript:
{transcript}

Instructions:

1. Identify the discussion of each participant.
2. Identify knowledge shared by each participant.
3. Identify action items assigned to each participant.
4. Generate an overall meeting summary.
5. Return ONLY valid JSON.
6. Do not include markdown.
7. Do not explain anything.

Expected JSON format:

{{
    "meeting_summary": [
        "summary point 1",
        "summary point 2"
    ],

    "employees": [

        {{
            "name": "Rohit Singh",

            "discussion": [
                "discussion"
            ],

            "knowledge_shared": [
                "knowledge"
            ],

            "action_items": [
                "task"
            ]
        }}

    ]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content.strip()

    # Remove markdown if present
    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    result = json.loads(content)

    os.makedirs("meeting/output", exist_ok=True)

    with open(
        "meeting/output/meeting_summary.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            result,
            f,
            indent=4,
            ensure_ascii=False
        )

    return result