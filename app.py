import streamlit as st
import requests
import json

# API Gateway GET endpoint
API_URL = "https://v98yls4aeg.execute-api.us-east-1.amazonaws.com/dev/kbquery"

st.set_page_config(page_title="CaseCrux KB Assistant", page_icon="🧠")
st.title("CaseCrux with Amazon Bedrock")
st.subheader("Legal Knowledge Assistant", divider="rainbow")

# Sidebar - clear chat option
if st.sidebar.button('🧹 Clear Chat History'):
    st.session_state.chat_history = []
    st.rerun()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# User prompt input
prompt = st.chat_input("Enter your legal question...")

if prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "text": prompt})

    try:
        # Send GET request
        response = requests.get(API_URL, params={"prompt": prompt})

        # Decode first layer (API Gateway response)
        outer = response.json()
        body_str = outer.get("body", "{}")

        # Decode second layer (actual payload from Lambda)
        data = json.loads(body_str)

        if response.status_code == 200:
            answer = data.get("answer", "No answer returned.")
            context = data.get("context", "")
            doc_url = data.get("doc_url", "")

            # Display assistant message
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "text": answer})

            # Display context and source
            if context and doc_url:
                st.markdown(f"<span style='color:#FFDA33'>Context used:</span> {context}", unsafe_allow_html=True)
                st.markdown(f"<span style='color:#FFDA33'>Source Document:</span> [View Source]({doc_url})", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color:red'>No context/source provided.</span>", unsafe_allow_html=True)
        else:
            st.error(f"Error: {data.get('error', 'Unknown error')}")

    except Exception as e:
        st.error(f"API call failed: {str(e)}")
