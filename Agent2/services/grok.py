import ollama


class GrokService:

    def __init__(self, model_name: str = "gemma3:1b"):
        self.model_name = model_name

    def generate(self, prompt: str) -> str:

        response = ollama.generate(
            model=self.model_name,
            prompt=prompt,
            format="json"
        )

        return response["response"]