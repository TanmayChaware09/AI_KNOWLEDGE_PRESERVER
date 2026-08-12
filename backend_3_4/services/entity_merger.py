class EntityMerger:

    PRIORITY = {

        "PERSON": 1,

        "EMAIL_ADDRESS": 2,

        "PHONE_NUMBER": 3,

        "LOCATION": 4

    }

    def merge(
        self,
        presidio_entities,
        grok_entities
    ):

        all_entities = list(
            presidio_entities
        ) + list(
            grok_entities
        )

        all_entities.sort(

            key=lambda entity: (

                entity.start,

                self.PRIORITY.get(
                    entity.entity_type,
                    999
                )

            )

        )

        merged = []

        occupied = []

        for entity in all_entities:

            overlap = False

            for start, end in occupied:

                if not (

                    entity.end <= start

                    or

                    entity.start >= end

                ):

                    overlap = True

                    break

            if overlap:

                continue

            merged.append(
                entity
            )

            occupied.append(

                (

                    entity.start,

                    entity.end

                )

            )

        return merged