from shared.contracts import (
    KnowledgeCard,
    SafeKnowledgeCard
)

from services.pii_detector import PIIDetector
from services.anonymizer import Anonymizer
from services.hashing_service import HashingService
from services.grok_service import GrokService


class PrivacyAgent:

    def __init__(self):

        self.detector = PIIDetector()

        self.anonymizer = Anonymizer()

        self.hasher = HashingService()

        self.grok = GrokService()

    def process(
        self,
        card: KnowledgeCard
    ) -> SafeKnowledgeCard:

        entities = self.detector.detect(
            card.summary
        )

        sanitized_summary = self.anonymizer.anonymize(
            card.summary,
            entities
        )

        self.grok.validate(
            card.summary,
            sanitized_summary
        )

        # Generated for Storage Agent workflow
        employee_hash = self.hasher.hash(
            card.employee_id
        )

        _ = employee_hash

        return SafeKnowledgeCard(

            title=card.title,

            summary=sanitized_summary,

            category=card.category,

            confidence=card.confidence,

            timestamp=card.timestamp

        )