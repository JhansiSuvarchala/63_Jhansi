import json
import warnings
warnings.filterwarnings("ignore")

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# -----------------------------
# Load & prepare drug documents
# -----------------------------
with open("data/drug_labels_sample.json") as f:
    drug_data = json.load(f)

documents = []
for d in drug_data:
    documents.append(
        f"""
        Drug: {d['drug']}
        Uses: {d['uses']}
        Dosage: {d['dosage']}
        Warnings: {d['warnings']}
        Side Effects: {d['side_effects']}
        """
    )

splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
docs = splitter.create_documents(documents)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever()

# -----------------------------
# ask_drug function (H2 outcome)
# -----------------------------
def ask_drug(question: str):
    results = retriever.invoke(question)
    if not results:
        return "No relevant drug information found."
    return results[0].page_content


# -----------------------------
# CLI-based user interaction
# -----------------------------
if __name__ == "__main__":
    print("\n💊 Medication Q&A Chatbot (type 'exit' to quit)\n")

    while True:
        user_question = input("User: ")

        if user_question.lower() == "exit":
            print("Chatbot: Stay healthy! 👋")
            break

        answer = ask_drug(user_question)
        print("\nChatbot:\n", answer)
