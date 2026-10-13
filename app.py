
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Admission FAQ Bot",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Admission FAQ Assistant")
st.write(
    "Ask me about college admissions, fees, cutoffs, "
    "courses, scholarships, placements, hostel and eligibility!"
)

SYSTEM_PROMPT = """
You are Admission FAQ Assistant, a helpful chatbot for college
admissions in India.

Help users with:
- Admission procedures and eligibility
- College courses and entrance exams
- Fees and scholarships
- Cutoffs and admission deadlines
- Placements and hostel facilities
- Required documents and application processes

Instructions:
1. Answer clearly in the language used by the user.
2. You can answer in English, Hindi or Marathi.
3. Explain admission procedures in simple language.
4. Never invent college-specific fees, cutoffs, placement
   statistics, deadlines or eligibility requirements.
5. If verified information is unavailable, clearly say so.
6. Recommend checking the official college website or
   official admission portal for the latest information.
7. Ask for the college name, course and admission year
   when those details are needed.
8. Do not claim to have checked a website unless you
   actually have access to its information.
"""

# Read the API key securely from Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.warning(
        "Gemini API key is not configured. "
        "Please add GEMINI_API_KEY in Streamlit Secrets."
    )

# Store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
question = st.chat_input("Ask your admission question...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    if not api_key:
        st.error(
            "API key missing. Please configure it in "
            "Streamlit Cloud → Settings → Secrets."
        )
    else:
        try:
            client = genai.Client(api_key=api_key)

            # Convert conversation history to Gemini format
            contents = []

            for message in st.session_state.messages:
                role = (
                    "model"
                    if message["role"] == "assistant"
                    else "user"
                )

                contents.append({
                    "role": role,
                    "parts": [{"text": message["content"]}]
                })

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=contents,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT,
                            temperature=0.3
                        )
                    )

                    answer = response.text

                    if not answer:
                        answer = (
                            "I could not generate an answer. "
                            "Please try asking another question."
                        )

                st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception:
            st.error(
                "Sorry, I could not get a response from Gemini. "
                "Please check your API key, model availability, "
                "API quota and network connection, then try again."
            )

# Clear conversation button
if st.session_state.messages:
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()
