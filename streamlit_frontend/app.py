import streamlit as st
import requests

API_URL = "https://pharma-ai-assistant-api.onrender.com"
st.set_page_config(
    page_title="AI-First CRM",
    page_icon="💊",
    layout="wide"
)

st.title("💊 AI-First CRM")
st.caption("HCP Log Interaction System")

left, right = st.columns([1, 1])

with left:

    st.subheader("📝 Log Interaction")

    hcp = st.text_input("HCP Name")

    interaction_type = st.selectbox(
        "Interaction Type",
        ["Meeting", "Call", "Email", "Conference"]
    )

    attendees = st.text_input("Attendees (comma separated)")

    topics = st.text_area("Topics Discussed")

    materials = st.text_input("Materials Shared")

    samples = st.text_input("Samples Distributed")

    sentiment = st.selectbox(
        "Sentiment",
        ["Positive", "Neutral", "Negative"]
    )

    outcomes = st.text_area("Outcomes")

    followups = st.text_input("Follow-up Actions")

    if st.button("Log Interaction"):

        payload = {
            "hcp_name": hcp,
            "interaction_type": interaction_type,
            "attendees": attendees.split(",") if attendees else [],
            "topics_discussed": topics,
            "materials_shared": materials.split(",") if materials else [],
            "samples_distributed": samples.split(",") if samples else [],
            "sentiment": sentiment.lower(),
            "outcomes": outcomes,
            "follow_up_actions": followups.split(",") if followups else []
        }

        response = requests.post(
            f"{API_URL}/api/interactions",
            json=payload
        )

        if response.status_code in [200, 201]:
            st.success("Interaction logged successfully!")
        else:
            st.error(response.text)

with right:

    st.subheader("🤖 AI Assistant")

    prompt = st.text_area(
        "Ask the AI",
        height=250
    )

    if st.button("Send"):

        response = requests.post(
            f"{API_URL}/api/chat",
            json={"message": prompt}
        )

        if response.status_code == 200:
            st.success("Reply")
            st.write(response.json())
        else:
            st.error(response.text)