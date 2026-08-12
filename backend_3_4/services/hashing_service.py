import hashlib


class HashingService:

    def hash(self, value: str) -> str:

        if not value:

            return ""

        return hashlib.sha256(

            value.encode("utf-8")

        ).hexdigest()