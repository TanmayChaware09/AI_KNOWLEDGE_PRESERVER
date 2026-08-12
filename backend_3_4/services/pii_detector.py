from services.presidio_service import PresidioService
from services.grok_service import GrokService
from services.entity_merger import EntityMerger


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

        # Version 0.0
        grok_entities = []

        return self.merger.merge(

            presidio_entities,

            grok_entities

        )