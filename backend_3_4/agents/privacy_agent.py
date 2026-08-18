from backend_3_4.shared.contracts import (
    KnowledgeCard,
    SafeKnowledgeCard
)

from backend_3_4.services.pii_detector import PIIDetector
from backend_3_4.services.anonymizer import Anonymizer
from backend_3_4.services.hashing_service import HashingService
from backend_3_4.services.grok_service import GrokService

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

            source=card.source,

            timestamp=card.timestamp

            
        )