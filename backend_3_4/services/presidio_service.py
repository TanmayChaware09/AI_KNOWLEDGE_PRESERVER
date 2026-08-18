from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import (
    NlpEngineProvider,
)


class PresidioService:

    def __init__(self):

        configuration = {
            "nlp_engine_name": "spacy",
            "models": [
                {
                    "lang_code": "en",
                    "model_name": "en_core_web_sm",
                }
            ],
        }

        provider = NlpEngineProvider(
            nlp_configuration=configuration
        )

        nlp_engine = provider.create_engine()

        self.analyzer = AnalyzerEngine(
            nlp_engine=nlp_engine
        )

    def detect(
        self,
        text: str
    ):

        return self.analyzer.analyze(
            text=text,
            language="en",
            entities=[
                "PERSON",
                "EMAIL_ADDRESS",
                "PHONE_NUMBER",
                "LOCATION"
            ]
        )
    