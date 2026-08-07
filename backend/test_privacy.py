from datetime import datetime

from agents.privacy_agent import PrivacyAgent

from shared.contracts import KnowledgeCard


agent = PrivacyAgent()

card = KnowledgeCard(

    title="VPN Issue",

    summary="""
    Rahul Sharma reported that his email is
    rahul@gmail.com

    Contact Number : 9876543210

    """,

    category="IT Support",

    confidence=0.98,

    source="Slack",

    employee_id="EMP001",

    timestamp=datetime.now()

)

result = agent.process(card)

print(result.model_dump())