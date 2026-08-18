from slack_sdk import WebClient
from dotenv import load_dotenv
from shared.contracts import RawDocument
from datetime import datetime
from pathlib import Path

import json
import os


load_dotenv()


def collect_slack():

    # ========================================================
    # STATE FILE
    # ========================================================

    state_path = (
        Path(__file__).resolve().parent.parent
        / "state"
        / "slack.json"
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
    # SLACK CLIENT
    # ========================================================

    client = WebClient(
        token=os.getenv("SLACK_BOT_TOKEN")
    )


    # ========================================================
    # GET CHANNELS
    # ========================================================

    channels = client.conversations_list()[
        "channels"
    ]


    raw_documents = []


    # ========================================================
    # PROCESS CHANNELS
    # ========================================================

    for channel in channels:

        try:

            history = client.conversations_history(
                channel=channel["id"]
            )


            for message in history["messages"]:

                # ------------------------------------------------
                # Skip Slack system messages
                # ------------------------------------------------

                if message.get("subtype"):
                    continue


                # ------------------------------------------------
                # Unique Slack message ID
                # ------------------------------------------------

                message_id = (
                    f"{channel['id']}:"
                    f"{message['ts']}"
                )


                # ------------------------------------------------
                # Skip already processed messages
                # ------------------------------------------------

                if message_id in processed_ids:
                    continue


                # ------------------------------------------------
                # Employee details
                # ------------------------------------------------

                employee_id = message.get(
                    "user",
                    "UNKNOWN"
                )

                employee_name = "Unknown"


                if employee_id != "UNKNOWN":

                    try:

                        user_info = (
                            client
                            .users_info(
                                user=employee_id
                            )
                        )

                        employee_name = (
                            user_info["user"]
                            .get(
                                "real_name",
                                "Unknown"
                            )
                        )

                    except Exception:

                        pass


                # ------------------------------------------------
                # Create RawDocument
                # ------------------------------------------------

                raw_doc = RawDocument(

                    source="slack",

                    employee_id=employee_id,

                    employee_name=employee_name,

                    department="Unknown",

                    content=(
                        f"Channel: "
                        f"{channel['name']}\n"
                        f"Message: "
                        f"{message.get('text', '')}"
                    ),

                    timestamp=(
                        datetime.fromtimestamp(
                            float(message["ts"])
                        )
                    ),

                    url=(
                        "https://slack.com/"
                        f"app_redirect?"
                        f"channel={channel['id']}"
                    )
                )


                # ------------------------------------------------
                # Add document
                # ------------------------------------------------

                raw_documents.append(
                    raw_doc
                )


                # ------------------------------------------------
                # Mark as processed
                # ------------------------------------------------

                processed_ids.add(
                    message_id
                )


        except Exception as e:

            # Bot may not be a member of channel
            continue


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
    # RETURN ONLY NEW DOCUMENTS
    # ========================================================

    return raw_documents


def run():

    return collect_slack()