import json
import re
import warnings
warnings.filterwarnings("ignore")

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# =========================================================
# Load cleaned openFDA dataset
# =========================================================
print("📂 Loading FDA dataset...")

with open("data/openfda_clean.json", "r") as f:
    data = json.load(f)

documents = []
for d in data:
    text = f"""
Drug: {d.get("drug_name", "")}

Uses:
{d.get("uses", "")}

Dosage:
{d.get("dosage", "")}

Warnings:
{d.get("warnings", "")}

Side Effects:
{d.get("side_effects", "")}
"""
    documents.append(text.strip())


# =========================================================
# Build / Load Vector Store
# =========================================================
print("📦 Loading / Creating vector database...")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=100
)

docs = splitter.create_documents(documents)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

# ---------------------------------------------------------
# SAFE BATCH INSERT (FIX)
# ---------------------------------------------------------
if vectorstore._collection.count() == 0:
    print("⏳ Building vector database (one-time)...")

    BATCH_SIZE = 500
    for i in range(0, len(docs), BATCH_SIZE):
        batch = docs[i:i + BATCH_SIZE]
        vectorstore.add_documents(batch)
        print(f"   ➕ Added batch {i // BATCH_SIZE + 1}")

    vectorstore.persist()
    print("✅ Vector database ready")
else:
    print("✅ Vector database loaded")

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})


# =========================================================
# Intent detection
# =========================================================
def detect_intent(question: str):
    q = question.lower()
    if any(x in q for x in ["dosage", "dose", "how much", "how many"]):
        return "Dosage"
    if any(x in q for x in ["use", "used for", "indication"]):
        return "Uses"
    if any(x in q for x in ["warning", "precaution", "safe"]):
        return "Warnings"
    if any(x in q for x in ["side effect", "adverse"]):
        return "Side Effects"
    if any(x in q for x in ["remind", "schedule"]):
        return "Reminder"
    return "General"


# =========================================================
# Extract drug name
# =========================================================
def extract_drug(question: str):
    words = re.findall(r"[a-zA-Z]{4,}", question.lower())
    ignore = {
        "dosage", "dose", "uses", "use",
        "side", "effects", "warning",
        "warnings", "remind", "schedule",
        "tablet", "capsule", "medicine"
    }
    candidates = [w for w in words if w not in ignore]
    return candidates[-1] if candidates else None


# =========================================================
# RAG-based Question Answering
# =========================================================
def ask_drug(question: str):
    intent = detect_intent(question)
    drug = extract_drug(question)

    if not drug:
        return "❌ Please mention a valid drug name."

    query = f"{drug} {intent}"
    results = retriever.invoke(query)

    if not results:
        return f"❌ No FDA drug information found for '{drug}'."

    content = results[0].page_content

    # Extract requested section
    lines = content.split("\n")
    capture = False
    output = []

    for line in lines:
        if intent.lower() in line.lower():
            capture = True
            continue
        if capture:
            if line.strip() == "":
                break
            output.append(line.strip())

    return "\n".join(output[:8]) if output else content


# =========================================================
# Reminder Agent
# =========================================================
def reminder_agent(question: str):
    drug = extract_drug(question)
    return {
        "medicine": drug.capitalize(),
        "schedule": ["08:00 AM", "02:00 PM", "08:00 PM"],
        "note": "Sample reminder generated from FDA drug label. Not medical advice."
    }


# =========================================================
# MAIN LOOP
# =========================================================
if __name__ == "__main__":
    print("\n💊 Medication Reminder Chatbot (H2)")
    print("Using real openFDA Drug Label dataset")
    print("Type 'exit' to quit")

    while True:
        user_input = input("\nUser: ").strip()

        if user_input.lower() == "exit":
            print("\nChatbot: Stay healthy 👋")
            break

        intent = detect_intent(user_input)

        if intent == "Reminder":
            print("\n🤖 Reminder Plan:")
            print(json.dumps(reminder_agent(user_input), indent=2))
        else:
            print("\n🤖 FDA Answer:")
            print(ask_drug(user_input))

        print("-" * 60)
