from backend_3_4.services.presidio_service import PresidioService
from backend_3_4.services.grok_service import GrokService
from backend_3_4.services.entity_merger import EntityMerger
class PIIDetector:

    def __init__(self):

        self.presidio = PresidioService()

        self.grok = GrokService()

        self.merger = EntityMerger()

    def detect(
        self,
        text: str
    ):

        presidio_entities = self.presidio.detect(
            text
    )

    # Known technology/product names that should
    # never be treated as personal names.
        protected_terms = {
        "anthropic claude",
        "claude",
        "chatgpt",
        "gemini",
        "openai",
        "google",
        "microsoft",
        "github",
        "slack",
        "ollama",
        "postgresql",
        "chromadb"
    }

        filtered_entities = []

        for entity in presidio_entities:

            detected_text = text[
            entity.start:entity.end
            ].strip().lower()

            if (
                entity.entity_type == "PERSON"
                and detected_text in protected_terms
            ):
                continue

            filtered_entities.append(entity)

    # Version 0.0
        grok_entities = []

        return self.merger.merge(
            filtered_entities,
            grok_entities
        )