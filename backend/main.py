import sys
from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# AGENT 1 : COLLECTORS
# ============================================================

from backend.collectors.email import run as gmail_run
from backend.collectors.github import run as github_run
from backend.collectors.slack import run as slack_run
from backend.collectors.meeting import run as meeting_run


# ============================================================
# AGENT 2 : KNOWLEDGE EXTRACTION
# ============================================================

from Agent2.agents.knowledge_agent import extract_knowledge


# ============================================================
# MAIN
# ============================================================

def main():

    # ========================================================
    # LOAD AGENT 3 + AGENT 4
    # ========================================================

    BACKEND_3_4 = PROJECT_ROOT / "backend_3_4"

    if str(BACKEND_3_4) not in sys.path:
        sys.path.insert(0, str(BACKEND_3_4))

    from agents.privacy_agent import PrivacyAgent
    from agents.storage_agent import StorageAgent

    privacy_agent = PrivacyAgent()
    storage_agent = StorageAgent()

    print("=" * 70)
    print("                 AI LOSS PREVENTION SYSTEM")
    print("=" * 70)


    # ========================================================
    # AGENT 1 : DATA COLLECTION
    # ========================================================

    print("\nStarting Gmail Collector...")

    gmail_docs = gmail_run()

    print(
        f"✓ Gmail Completed "
        f"({len(gmail_docs)} new documents)"
    )


    print("\nStarting GitHub Collector...")

    github_docs = github_run()

    print(
        f"✓ GitHub Completed "
        f"({len(github_docs)} new documents)"
    )


    print("\nStarting Slack Collector...")

    slack_docs = slack_run()

    print(
        f"✓ Slack Completed "
        f"({len(slack_docs)} new documents)"
    )


    print("\nStarting Meeting Collector...")

    meeting_docs = meeting_run()

    if isinstance(meeting_docs, list):
        meeting_count = len(meeting_docs)

    elif meeting_docs:
        meeting_count = 1

    else:
        meeting_count = 0


    print(
        f"✓ Meeting Completed "
        f"({meeting_count} new documents)"
    )


    # ========================================================
    # MERGE RAW DOCUMENTS
    # ========================================================

    all_documents = []

    all_documents.extend(gmail_docs)

    all_documents.extend(github_docs)

    all_documents.extend(slack_docs)


    if meeting_docs:

        if isinstance(
            meeting_docs,
            list
        ):

            all_documents.extend(
                meeting_docs
            )

        elif hasattr(
            meeting_docs,
            "source"
        ):

            all_documents.append(
                meeting_docs
            )


    # ========================================================
    # AGENT 1 SUMMARY
    # ========================================================

    print("\n" + "=" * 70)
    print("AGENT 1 : RAW DOCUMENTS")
    print("=" * 70)


    print(
        f"\nNew Raw Documents : "
        f"{len(all_documents)}"
    )


    for i, doc in enumerate(
        all_documents,
        start=1
    ):

        print(
            f"\nDocument {i}"
        )

        print("-" * 70)

        print(
            f"Source      : "
            f"{doc.source}"
        )

        print(
            f"Employee    : "
            f"{doc.employee_name}"
        )

        print(
            f"Employee ID : "
            f"{doc.employee_id}"
        )

        print(
            f"Department  : "
            f"{doc.department}"
        )

        print(
            f"Timestamp   : "
            f"{doc.timestamp}"
        )

        print(
            f"URL         : "
            f"{doc.url}"
        )

        print("\nContent:")

        print(
            doc.content
        )


    # ========================================================
    # AGENT 2 : KNOWLEDGE EXTRACTION
    # ========================================================

    print("\n" + "=" * 70)
    print("AGENT 2 : KNOWLEDGE EXTRACTION")
    print("=" * 70)


    print(
        f"\nProcessing "
        f"{len(all_documents)} RawDocuments..."
    )


    knowledge_cards = []

    failed_extractions = 0


    if not all_documents:

        print(
            "\nNo new documents found."
        )

        print(
            "Agent 2 skipped."
        )


    else:

        for i, document in enumerate(
            all_documents,
            start=1
        ):

            print(
                f"\n[{i}/{len(all_documents)}] "
                f"Processing {document.source}"
            )

            print(
                f"Employee : "
                f"{document.employee_name}"
            )

            print(
                f"Employee ID : "
                f"{document.employee_id}"
            )


            try:

                # ====================================================
                # NEW AGENT 2
                # One RawDocument → MANY KnowledgeCards
                # ====================================================

                extracted_cards = extract_knowledge(
                    document
                )


                if not isinstance(
                    extracted_cards,
                    list
                ):

                    raise ValueError(
                        "Agent 2 must return a list of KnowledgeCards."
                    )


                # ====================================================
                # NO KNOWLEDGE
                # ====================================================

                if not extracted_cards:

                    print(
                        "⚠ No valuable institutional knowledge found"
                    )

                    continue


                # ====================================================
                # PROCESS ALL CARDS
                # ====================================================

                for card_number, knowledge_card in enumerate(
                    extracted_cards,
                    start=1
                ):

                    # ------------------------------------------------
                    # QUALITY GATE
                    # ------------------------------------------------

                    if (
                        knowledge_card.title
                        == "No Valuable Knowledge"
                        or knowledge_card.confidence == 0.0
                    ):

                        print(
                            f"⚠ Card {card_number}: "
                            "No valuable knowledge"
                        )

                        continue


                    knowledge_cards.append(
                        knowledge_card
                    )


                    print(
                        f"\n✓ Knowledge Card "
                        f"{card_number} extracted"
                    )

                    print(
                        f"  Title      : "
                        f"{knowledge_card.title}"
                    )

                    print(
                        f"  Category   : "
                        f"{knowledge_card.category}"
                    )

                    print(
                        f"  Confidence : "
                        f"{knowledge_card.confidence}"
                    )

                    print(
                        f"  Source     : "
                        f"{knowledge_card.source}"
                    )


            except Exception as e:

                failed_extractions += 1

                print(
                    "✗ Knowledge extraction failed"
                )

                print(
                    f"  Error: {e}"
                )


    # ========================================================
    # AGENT 2 RESULTS
    # ========================================================

    print("\n" + "=" * 70)
    print("AGENT 2 : KNOWLEDGE CARDS")
    print("=" * 70)


    if not knowledge_cards:

        print(
            "\nNo new Knowledge Cards generated."
        )


    else:

        print(
            f"\nTotal Knowledge Cards : "
            f"{len(knowledge_cards)}"
        )


        for i, card in enumerate(
            knowledge_cards,
            start=1
        ):

            print(
                f"\nKnowledge Card {i}"
            )

            print("-" * 70)

            print(
                f"Title      : "
                f"{card.title}"
            )

            print(
                f"Summary    : "
                f"{card.summary}"
            )

            print(
                f"Category   : "
                f"{card.category}"
            )

            print(
                f"Confidence : "
                f"{card.confidence}"
            )

            print(
                f"Source     : "
                f"{card.source}"
            )

            print(
                f"Employee ID: "
                f"{card.employee_id}"
            )

            print(
                f"Timestamp  : "
                f"{card.timestamp}"
            )


    # ========================================================
    # AGENT 3 + AGENT 4
    # ========================================================

    print("\n" + "=" * 70)
    print("AGENT 3 : PRIVACY + AGENT 4 : STORAGE")
    print("=" * 70)


    stored_count = 0

    failed_storage = 0


    if not knowledge_cards:

        print(
            "\nNo Knowledge Cards available."
        )

        print(
            "Agent 3 and Agent 4 skipped."
        )


    else:

        for i, card in enumerate(
            knowledge_cards,
            start=1
        ):

            print(
                f"\n[{i}/{len(knowledge_cards)}] "
                f"Processing Knowledge Card"
            )

            print(
                f"Title : "
                f"{card.title}"
            )


            try:

                # ====================================================
                # AGENT 3 : PRIVACY
                # ====================================================

                print(
                    "\nAgent 3 : Detecting PII..."
                )


                safe_card = privacy_agent.process(
                    card
                )


                print(
                    "✓ Privacy processing completed"
                )


                print(
                    f"  Safe Title   : "
                    f"{safe_card.title}"
                )


                print(
                    f"  Safe Summary : "
                    f"{safe_card.summary}"
                )


                # ====================================================
                # EMPLOYEE HASH
                # ====================================================

                employee_hash = (
                    privacy_agent.hasher.hash(
                        card.employee_id
                    )
                )


                # ====================================================
                # AGENT 4 : STORAGE
                # ====================================================

                print(
                    "\nAgent 4 : Storing knowledge..."
                )


                stored = storage_agent.store(

                    card=safe_card,

                    employee_hash=employee_hash

                )


                if stored.stored:

                    stored_count += 1


                    print(
                        "✓ Knowledge stored successfully"
                    )


                    print(
                        f"  PostgreSQL ID : "
                        f"{stored.postgres_id}"
                    )


                    print(
                        f"  Chroma Vector : "
                        f"{stored.vector_id}"
                    )


            except Exception as e:

                failed_storage += 1


                print(
                    "✗ Agent 3/4 processing failed"
                )


                print(
                    f"  Error: {e}"
                )


    # ========================================================
    # FINAL SYSTEM SUMMARY
    # ========================================================

    print("\n" + "=" * 70)
    print("AI LOSS PREVENTION SYSTEM COMPLETED")
    print("=" * 70)


    print(
        f"Gmail Documents       : "
        f"{len(gmail_docs)}"
    )


    print(
        f"GitHub Documents      : "
        f"{len(github_docs)}"
    )


    print(
        f"Slack Documents       : "
        f"{len(slack_docs)}"
    )


    print(
        f"Meeting Documents     : "
        f"{meeting_count}"
    )


    print("-" * 70)


    print(
        f"Total New Documents   : "
        f"{len(all_documents)}"
    )


    print(
        f"Knowledge Cards       : "
        f"{len(knowledge_cards)}"
    )


    print(
        f"Failed Extractions    : "
        f"{failed_extractions}"
    )


    print(
        f"Stored Knowledge      : "
        f"{stored_count}"
    )


    print(
        f"Failed Agent 3/4      : "
        f"{failed_storage}"
    )


    # ========================================================
    # SYSTEM STATUS
    # ========================================================

    print("\n" + "=" * 70)


    total_failures = (
        failed_extractions
        + failed_storage
    )


    if total_failures == 0:

        print(
            "SYSTEM STATUS : SUCCESS"
        )

    else:

        print(
            "SYSTEM STATUS : COMPLETED WITH ERRORS"
        )


    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()