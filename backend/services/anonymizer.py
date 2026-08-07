class Anonymizer:

    def anonymize(

        self,

        text: str,

        entities

    ):

        entities = sorted(

            entities,

            key=lambda entity: entity.start,

            reverse=True

        )

        for entity in entities:

            replacement = "[REDACTED]"

            text = (

                text[:entity.start]

                + replacement

                + text[entity.end:]

            )

        return text