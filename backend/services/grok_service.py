from config.settings import settings


class GrokService:

    def __init__(self):

        self.api_key = settings.GROK_API_KEY

    def validate(

        self,

        original_text: str,

        anonymized_text: str

    ) -> bool:

        """
        Version 0.0

        Placeholder for Grok validation.

        Future:
        Send both texts to Grok and verify
        that all sensitive information
        has been removed without changing
        business meaning.
        """

        return True