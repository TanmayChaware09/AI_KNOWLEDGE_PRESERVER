import json
from meeting.meeting_llm import analyze_meeting
from pathlib import Path

def extract_meeting_knowledge(transcript):

    participants_path = (
        Path(__file__).resolve().parent
        / "participants.json"
    )

    with open(
        participants_path,
        "r",
        encoding="utf-8"
    ) as f:
        participants = json.load(f)
    meeting = {
        "meeting_id": participants["meeting_id"],
        "title": "Weekly Engineering Meeting",
        "manager": "Rahul Sharma",
        "participants": participants["participants"]
    }   

    result = analyze_meeting(
        transcript,
        meeting
    )

    with open(
        "meeting/output/knowledge.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            result,
            f,
            indent=4
        )

    print("\nKnowledge extracted successfully!")

    return result