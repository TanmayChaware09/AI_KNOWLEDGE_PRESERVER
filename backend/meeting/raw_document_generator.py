import json
from datetime import datetime

from shared.contracts import RawDocument


def generate_raw_documents():

    with open(
        "meeting/output/meeting_summary.json",
        "r",
        encoding="utf-8"
    ) as f:

        meeting = json.load(f)

    raw_documents = []

    meeting_summary = "\n".join(
        meeting.get("meeting_summary", [])
    )

    for employee in meeting["employees"]:

        discussion = "\n".join(
            f"• {x}"
            for x in employee.get("discussion", [])
        )

        knowledge = "\n".join(
            f"• {x}"
            for x in employee.get("knowledge_shared", [])
        )

        actions = "\n".join(
            f"• {x}"
            for x in employee.get("action_items", [])
        )

        content = f"""
Meeting Summary

{meeting_summary}

Discussion

{discussion}

Knowledge Shared

{knowledge}

Action Items

{actions}
""".strip()

        raw_documents.append(

            RawDocument(

                source="meeting",

                employee_id=employee["name"],

                employee_name=employee["name"],

                department="Unknown",

                content=content,

                timestamp=datetime.now(),

                url="meeting/recordings/weekly_meeting.mp3"

            )

        )

    return raw_documents