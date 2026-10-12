
import streamlit as st

st.set_page_config(
    page_title="Admission FAQ Bot",
    page_icon="🎓"
)

st.title("🎓 Admission FAQ Assistant")
st.write("Ask me about college admissions!")

faqs = {
    "admission": "Please check the official admission process and eligibility criteria.",
    "documents": "Common documents include marksheets, leaving certificate, and identity proof. Check your college's official list.",
    "fees": "Please check the latest official college fee structure.",
    "courses": "Please refer to the college's official website for available courses."
}

question = st.chat_input("Ask your admission question...")

if question:
    st.chat_message("user").write(question)

    answer = "I could not find this information. Please contact the college admission office."

    for keyword, response in faqs.items():
        if keyword in question.lower():
            answer = response
            break

    with st.chat_message("assistant"):
        st.write(answer)
