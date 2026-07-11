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


# ==========================
# LOG INTERACTION SECTION
# ==========================

with left:

    st.subheader("📝 Log Interaction")

    hcp = st.text_input("HCP Name")

    interaction_type = st.selectbox(
        "Interaction Type",
        ["Meeting", "Call", "Email", "Conference"]
    )

    attendees = st.text_input(
        "Attendees (comma separated)"
    )

    topics = st.text_area(
        "Topics Discussed"
    )

    materials = st.text_input(
        "Materials Shared"
    )

    samples = st.text_input(
        "Samples Distributed"
    )

    sentiment = st.selectbox(
        "Sentiment",
        ["Positive", "Neutral", "Negative"]
    )

    outcomes = st.text_area(
        "Outcomes"
    )

    followups = st.text_input(
        "Follow-up Actions"
    )


    if st.button("Log Interaction"):

        payload = {
            "hcp_name": hcp,
            "interaction_type": interaction_type,
            "attendees": [
                x.strip()
                for x in attendees.split(",")
            ] if attendees else [],

            "topics_discussed": topics,

            "materials_shared": [
                x.strip()
                for x in materials.split(",")
            ] if materials else [],

            "samples_distributed": [
                x.strip()
                for x in samples.split(",")
            ] if samples else [],

            "sentiment": sentiment.lower(),

            "outcomes": outcomes,

            "follow_up_actions": [
                x.strip()
                for x in followups.split(",")
            ] if followups else []
        }


        try:

            response = requests.post(
                f"{API_URL}/api/interactions",
                json=payload,
                timeout=30
            )


            if response.status_code in [200, 201]:

                st.success(
                    "✅ Interaction logged successfully!"
                )

                st.write(
                    "Saved interaction:"
                )

                st.json(
                    response.json()
                )


            else:

                st.error(
                    f"Backend returned error: {response.status_code}"
                )

                st.write(
                    response.text
                )


        except requests.exceptions.Timeout:

            st.error(
                "⏳ Backend took too long to respond. Try again."
            )


        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Cannot connect to backend."
            )


        except Exception as e:

            st.error(
                "Unexpected error occurred"
            )

            st.write(e)



# ==========================
# AI ASSISTANT SECTION
# ==========================

with right:

    st.subheader("🤖 AI Assistant")

    prompt = st.text_area(
        "Ask the AI",
        height=250
    )


    if st.button("Send"):

        if not prompt.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            try:

                response = requests.post(
                    f"{API_URL}/api/chat",
                    json={
                        "message": prompt
                    },
                    timeout=30
                )


                if response.status_code == 200:

                    st.success(
                        "AI Response"
                    )

                    st.write(
                        response.json()
                    )


                else:

                    st.error(
                        f"Chat API error: {response.status_code}"
                    )

                    st.write(
                        response.text
                    )


            except requests.exceptions.Timeout:

                st.error(
                    "AI service timed out."
                )


            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to AI backend."
                )


            except Exception as e:

                st.error(
                    "Unexpected error occurred"
                )

                st.write(e)