def medication_agent(user_query):
    if "remind" in user_query.lower() or "schedule" in user_query.lower():
        return {
            "medicine": "Paracetamol",
            "dosage": "500mg",
            "schedule": ["08:00 AM", "02:00 PM", "08:00 PM"],
            "note": "General reminder. Not a substitute for medical advice."
        }
    return None


if __name__ == "__main__":
    user_input = input("User: ")
    response = medication_agent(user_input)

    if response:
        print("\n🤖 Reminder Plan:\n", response)
    else:
        print("\n🤖 This query is handled by the drug Q&A system.")
