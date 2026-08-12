from datetime import datetime

from agents.privacy_agent import PrivacyAgent
from agents.storage_agent import StorageAgent

from shared.contracts import KnowledgeCard


def main():

    privacy = PrivacyAgent()

    storage = StorageAgent()

    card = KnowledgeCard(

        employee_id="EMP001",

        title="OAuth Login Issue",

        summary="""
        Rahul Sharma reported that
        rahul@gmail.com
        was unable to login.

        Contact:
        9876543210
        """,

        category="Authentication",

        confidence=0.96,

        source="Slack",

        timestamp=datetime.now()

    )

    safe_card = privacy.process(card)

    employee_hash = privacy.hasher.hash(
        card.employee_id
    )

    storage.store(

        card=safe_card,

        employee_hash=employee_hash

    )

    print("Pipeline Completed Successfully")


if __name__ == "__main__":

    main()