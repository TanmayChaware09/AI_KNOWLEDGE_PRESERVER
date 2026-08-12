from agents.retrieval_agent import retrieve


def generate_answer(query: str) -> str:
    """
    Generate a response using the retrieved knowledge cards.
    """

    documents = retrieve(query)

    if not documents:
        return "No relevant knowledge found."

    answer = "Answer:\n\n"

    for i, doc in enumerate(documents, start=1):
        answer += f"{i}. {doc}\n"

    return answer


if __name__ == "__main__":

    query = input("Ask a question: ")

    response = generate_answer(query)

    print("\n" + response)