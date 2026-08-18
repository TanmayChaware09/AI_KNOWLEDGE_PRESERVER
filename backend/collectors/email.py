import os
import re
import base64
import email.utils
import json

from datetime import datetime
from bs4 import BeautifulSoup
from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from shared.contracts import RawDocument

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]


def extract_text(part):
    data = part.get("body", {}).get("data")

    if not data:
        return ""

    text = base64.urlsafe_b64decode(
        data.encode("UTF-8")
    ).decode("utf-8", errors="ignore")

    if part.get("mimeType") == "text/html":
        text = BeautifulSoup(
            text,
            "html.parser"
        ).get_text(separator="\n")

    return text.strip()


def clean_email_body(text):

    # Remove HTML comments
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)

    # Remove URLs
    text = re.sub(r"https?://\S+", "", text)

    # Remove anything inside <>
    text = re.sub(r"<[^>]*>", "", text)

    # Remove standalone <
    text = text.replace("<", "")

    # Remove standalone >
    text = text.replace(">", "")

    # Remove image placeholders
    text = re.sub(r"\[image:.*?\]", "", text)

    # Remove invisible unicode characters
    text = re.sub(r"[\u200b-\u200f\u2060\ufeff]", "", text)

    # Normalize newlines
    text = text.replace("\r", "")

    # Remove repeated spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove repeated blank lines
    text = re.sub(r"\n{2,}", "\n\n", text)

    # Strip every line
    lines = [line.strip() for line in text.split("\n")]

    # Remove empty lines
    lines = [line for line in lines if line]

    return "\n".join(lines)

def collect_email():

    # ========================================================
    # STATE FILE
    # ========================================================

    state_path = (
        Path(__file__).resolve().parent.parent
        / "state"
        / "gmail.json"
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
    # GMAIL AUTHENTICATION
    # ========================================================

    creds = None

    token_path = (
        Path(__file__).resolve().parent.parent
        / "token.json"
    )

    if token_path.exists():

        creds = Credentials.from_authorized_user_file(
            str(token_path),
            SCOPES
        )

    print(
        "Creds exists :",
        creds is not None
    )

    if creds:

        print(
            "Valid        :",
            creds.valid
        )

        print(
            "Expired      :",
            creds.expired
        )

        print(
            "RefreshToken :",
            creds.refresh_token is not None
        )


    # ========================================================
    # AUTHENTICATE ONLY IF NEEDED
    # ========================================================

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            print(
                "Refreshing existing token..."
            )

            creds.refresh(
                Request()
            )

        else:

            print(
                "Opening browser for authentication..."
            )

            client_secret_path = (
                Path(__file__).resolve().parent.parent
                / "client_secret.json"
            )

            flow = (
                InstalledAppFlow
                .from_client_secrets_file(
                    str(client_secret_path),
                    SCOPES
                )
            )

            creds = flow.run_local_server(
                port=8080
            )


        # Save refreshed/new token

        with open(
            token_path,
            "w",
            encoding="utf-8"
        ) as token:

            token.write(
                creds.to_json()
            )


    # ========================================================
    # BUILD GMAIL SERVICE
    # ========================================================

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )


    # ========================================================
    # GET EMAILS
    # ========================================================

    results = (
        service
        .users()
        .messages()
        .list(
            userId="me",
            maxResults=5
        )
        .execute()
    )

    messages = results.get(
        "messages",
        []
    )


    raw_documents = []


    # ========================================================
    # PROCESS ONLY NEW EMAILS
    # ========================================================

    for msg in messages:

        message_id = msg["id"]


        # ----------------------------------------------------
        # SKIP ALREADY PROCESSED EMAIL
        # ----------------------------------------------------

        if message_id in processed_ids:

            continue


        try:

            # ------------------------------------------------
            # GET FULL EMAIL
            # ------------------------------------------------

            email_data = (
                service
                .users()
                .messages()
                .get(
                    userId="me",
                    id=message_id,
                    format="full"
                )
                .execute()
            )


            # ------------------------------------------------
            # HEADERS
            # ------------------------------------------------

            headers = (
                email_data[
                    "payload"
                ].get(
                    "headers",
                    []
                )
            )


            subject = "No Subject"

            sender = "Unknown Sender"

            date = datetime.now()


            for header in headers:

                if header["name"] == "Subject":

                    subject = header["value"]


                elif header["name"] == "From":

                    sender = header["value"]


                elif header["name"] == "Date":

                    try:

                        date = (
                            email.utils
                            .parsedate_to_datetime(
                                header["value"]
                            )
                        )

                    except Exception:

                        pass


            # ------------------------------------------------
            # EXTRACT BODY
            # ------------------------------------------------

            body = ""

            payload = email_data.get(
                "payload",
                {}
            )


            if "parts" in payload:

                for part in payload["parts"]:

                    if part.get("mimeType") in [
                        "text/plain",
                        "text/html"
                    ]:

                        body = extract_text(
                            part
                        )

                        if body:

                            break


            else:

                body = extract_text(
                    payload
                )


            # ------------------------------------------------
            # CLEAN BODY
            # ------------------------------------------------

            body = clean_email_body(
                body
            )


            # ------------------------------------------------
            # CREATE RAW DOCUMENT
            # ------------------------------------------------

            raw_doc = RawDocument(

                source="email",

                employee_id=(
                    "rohitkumar186singh@gmail.com"
                ),

                employee_name="Rohit Singh",

                department="Unknown",

                content=f"""
From: {sender}

Subject: {subject}

Body:
{body}
""".strip(),

                timestamp=date,

                url="https://mail.google.com/"
            )


            # ------------------------------------------------
            # ADD TO NEW DOCUMENTS
            # ------------------------------------------------

            raw_documents.append(
                raw_doc
            )


            # ------------------------------------------------
            # MARK AS PROCESSED
            # ------------------------------------------------

            processed_ids.add(
                message_id
            )


        except Exception as e:

            print(
                f"Skipping email: {e}"
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
    # RETURN ONLY NEW DOCUMENTS
    # ========================================================

    return raw_documents

def run():
    return collect_email()