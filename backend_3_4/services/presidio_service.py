from presidio_analyzer import AnalyzerEngine


class PresidioService:

    def __init__(self):

        self.analyzer = AnalyzerEngine()

    def detect(

        self,

        text: str

    ):

        return self.analyzer.analyze(

            text=text,

            language="en"

        )