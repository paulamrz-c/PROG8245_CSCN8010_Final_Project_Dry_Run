import streamlit as st
import requests
import re

API_URL = "http://localhost:8000/predict"

# Set page title
st.set_page_config(page_title="Student FAQ Chatbot", layout="centered")


# Start History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Convert URLs to Markdown links
def auto_convert_links(text: str) -> str:
    return re.sub(r'(https?://[^\s\)\]]+)', r'[\1](\1)', text)

# Title and instructions
st.title("🎓 AI Student Support Chatbot 🤖")
st.caption("Ask me anything. I’ll try to find the most relevant FAQ or student resource.")


# Showing History
# Showing History
for sender, message in st.session_state.messages:
    if "[" not in message and "]" not in message and "http" in message:
        message = auto_convert_links(message)

    if sender == "user":
        st.markdown(f"""
        <div style="text-align: right; margin-bottom: 10px;">
            <span style="background-color: #DDC7EF; color: #3E1A5B; padding: 10px 15px; border-radius: 13px; display: inline-block; max-width: 80%;">
                {message}
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="text-align: left; margin-bottom: 10px;">
            <span style="background-color: #B280DB; color: #3E1A5B; padding: 10px 15px; border-radius: 13px; display: inline-block; max-width: 80%;">
                {message}
            </span>
        </div>
        """, unsafe_allow_html=True)



with st.form(key="chat_form", clear_on_submit=True):
    # User input
    query = st.text_input("💬 Type your message:", key="chat_input")
    submitted = st.form_submit_button("Send")
    # On button click
    if submitted and query.strip():
        st.session_state.messages.append(("user", query))

        try:
            with st.spinner("Thinking..."):
                res = requests.post(API_URL, json={"question": query})
                if res.status_code == 200:
                    out = res.json()
                    reply = out['answer']
                else:
                    reply = "❌ API error. Please try again."
        except:
            reply = "🚫 Unable to reach the backend."

        st.session_state.messages.append(("bot", reply))
        st.rerun()
