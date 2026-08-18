import json
from pathlib import Path

from faster_whisper import WhisperModel

from connectors.google_drive import (
    get_latest_meeting,
    download_file
)

from meeting.knowledge_extractor import (
    extract_meeting_knowledge
)

from meeting.raw_document_generator import (
    generate_raw_documents
)


def collect_meeting():

    print("\nChecking Google Drive for Meeting Recordings...")


    # ========================================================
    # STATE FILE
    # ========================================================

    state_path = (
        Path(__file__).resolve().parent.parent
        / "state"
        / "meetings.json"
    )

    if state_path.exists():

        with open(
            state_path,
            "r",
            encoding="utf-8"
        ) as f:

            state = json.load(f)

    else:

        state = {
            "processed_ids": []
        }

    processed_ids = set(
        state.get("processed_ids", [])
    )


    # ========================================================
    # FIND LATEST MEETING
    # ========================================================

    meeting_file = get_latest_meeting()


    # ========================================================
    # LOAD MEETING METADATA
    # ========================================================

    metadata_path = (
        Path(__file__).resolve().parent.parent
        / "meeting"
        / "metadata"
        / "weekly_meeting.json"
    )


    with open(
        metadata_path,
        "r",
        encoding="utf-8"
    ) as f:

        meeting = json.load(f)


    meeting_id = str(
        meeting["meeting_id"]
    )


    # ========================================================
    # CHECK IF MEETING WAS ALREADY PROCESSED
    # ========================================================

    if meeting_id in processed_ids:

        print(
            f"Meeting {meeting_id} "
            "already processed. Skipping."
        )

        return []


    # ========================================================
    # GET RECORDING
    # ========================================================

    if meeting_file is None:

        print(
            "No Meeting Recording Found."
        )

        recording_path = (
            Path(__file__).resolve().parent.parent
            / "meeting"
            / "recordings"
            / meeting["recording"]
        )

    else:

        print(
            f"\nMeeting Found : "
            f"{meeting_file['name']}"
        )

        download_file(
            meeting_file["id"],
            meeting_file["name"]
        )

        recording_path = (
            Path(__file__).resolve().parent.parent
            / "meeting"
            / "recordings"
            / meeting_file["name"]
        )


    # ========================================================
    # MEETING DETAILS
    # ========================================================

    print("\nMeeting Details")
    print("---------------------------")

    print(
        "Meeting ID :",
        meeting["meeting_id"]
    )

    print(
        "Title      :",
        meeting["title"]
    )

    print(
        "Manager    :",
        meeting["manager"]
    )


    print("\nParticipants")

    for participant in meeting["participants"]:

        print(
            participant["id"],
            participant["name"]
        )


    # ========================================================
    # TRANSCRIPTION
    # ========================================================

    print("\nGenerating Transcript...")


    model = WhisperModel(
        "base",
        device="cpu",
        compute_type="int8"
    )


    segments, info = model.transcribe(
        str(recording_path)
    )


    transcript = ""


    transcript_path = (
        Path(__file__).resolve().parent.parent
        / "meeting"
        / "transcripts"
        / "weekly_meeting.txt"
    )


    with open(
        transcript_path,
        "w",
        encoding="utf-8"
    ) as f:

        for segment in segments:

            line = (
                f"[{segment.start:.2f} - "
                f"{segment.end:.2f}] "
                f"{segment.text}"
            )

            transcript += (
                line + "\n"
            )

            print(line)

            f.write(
                line + "\n"
            )


    print(
        "\nTranscript Saved Successfully!"
    )


    # ========================================================
    # MEETING KNOWLEDGE EXTRACTION
    # ========================================================

    extract_meeting_knowledge(
        transcript
    )


    # ========================================================
    # GENERATE RAW DOCUMENTS
    # ========================================================

    meeting_documents = (
        generate_raw_documents()
    )


    print(
        "\nMeeting Knowledge "
        "Generated Successfully!"
    )


    # ========================================================
    # MARK MEETING AS PROCESSED
    # ========================================================

    processed_ids.add(
        meeting_id
    )


    # ========================================================
    # SAVE STATE
    # ========================================================

    with open(
        state_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {
                "processed_ids": list(
                    processed_ids
                )
            },
            f,
            indent=4
        )


    # ========================================================
    # IMPORTANT:
    # RETURN RAW DOCUMENTS, NOT MEETING DICT
    # ========================================================

    return meeting_documents


def run():

    return collect_meeting()


if __name__ == "__main__":

    run()