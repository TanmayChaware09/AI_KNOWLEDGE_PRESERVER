from datetime import datetime

from agents.storage_agent import StorageAgent

from shared.contracts import SafeKnowledgeCard


agent = StorageAgent()


card = SafeKnowledgeCard(

    title="VPN Issue",

    summary="""
    Employee reported VPN is not working.

    Email and phone number have already been removed.

    """,

    category="IT Support",

    confidence=0.98,

    timestamp=datetime.now()

)


result = agent.store(

    card=card,

    employee_hash="6d8f1b2d7a6b9f8c",

    manager_hash="2e9c4d5f8a7b1c3d"

)


print(result.model_dump())