import ollama


class GrokService:

    def __init__(
        self,
        model_name: str = "gemma3:1b"
    ):
        self.model_name = model_name

    def generate(
        self,
        prompt: str
    ) -> str:

        try:

            # ====================================================
            # LOW-MEMORY OLLAMA CONFIGURATION
            # ====================================================
            #
            # num_ctx:
            # Keeps the context window small so the local model
            # does not consume unnecessary RAM.
            #
            # num_gpu:
            # Force CPU execution to avoid CUDA/CUDA_Host memory
            # allocation problems on the current machine.
            #
            # temperature:
            # Keeps RAG answers deterministic.
            # ====================================================

            response = ollama.generate(

                model=self.model_name,

                prompt=prompt,

                options={
                    "num_ctx": 1024,
                    "num_gpu": 0,
                    "temperature": 0.1,
                },

                keep_alive="5m",

            )


            return response.get(
                "response",
                ""
            )


        except Exception as e:

            print(
                "\n========================================"
            )

            print(
                "OLLAMA GENERATION ERROR"
            )

            print(
                "========================================"
            )

            print(
                str(e)
            )

            print(
                "========================================\n"
            )

            raise