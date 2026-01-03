💊 Medication Reminder Chatbot using RAG

📌 Problem Statement

Patients often face difficulties in understanding medication instructions such as dosage, usage, warnings, and side effects. Additionally, many patients forget to take medicines on time, which can lead to improper treatment and health risks.

🎯 Objective

To build an AI-powered Medication Reminder Chatbot that:

Answers drug-related questions using official FDA drug labels

Avoids hallucinations by relying only on verified data

Generates a safe sample medication reminder schedule

Uses Retrieval-Augmented Generation (RAG) for accurate responses

📂 Dataset

Dataset: openFDA Drug Label Dataset

Source: https://open.fda.gov/apis/drug/label/download/

Data Used: Cleaned subset of FDA drug labels (JSON format)

🧠 Solution Overview

This project uses a Retrieval-Augmented Generation (RAG) approach:

Drug label data is cleaned and chunked

Text chunks are converted into embeddings

Embeddings are stored in ChromaDB

User queries retrieve the most relevant FDA label sections

A lightweight agent detects reminder intent and returns a structured reminder plan

⚙️ Tech Stack

Language: Python

Framework: LangChain

Vector Store: ChromaDB

Embeddings: Sentence Transformers

Dataset: openFDA Drug Label Data

📤 Sample Features

Drug usage, dosage, warnings, and side effects Q&A

Label-aware responses (no hallucination)

Sample medication reminder generation (JSON output)

🎥 Demo Video

A 10-minute screen-recorded demo video with voice explanation will be shared via YouTube (Unlisted) as per hackathon guidelines.

⚠️ Disclaimer

This chatbot is for educational purposes only and is not a substitute for professional medical advice.
