import streamlit as st
from openai import OpenAI

st.title("💬 Chatbot mit OpenAI Assistant")
st.write(
    "Dieser Chatbot nutzt einen vordefinierten OpenAI Assistant (ID: asst_6eb9KdjXtWz5D9a1EFn2MCPD)."
)

# OpenAI API-Key
openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Bitte gib deinen OpenAI API Key ein, um fortzufahren.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # Sitzung für Nachrichten
    if "thread_id" not in st.session_state:
        # Erstelle einen neuen Thread (Konversation)
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id

    # Nachrichtenverlauf anzeigen
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Eingabe des Benutzers
    if prompt := st.chat_input("Was möchtest du fragen?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Nachricht an Thread anhängen
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=prompt,
        )

        # Assistant ausführen
        run = client.beta.threads.runs.create_and_poll(
            thread_id=st.session_state.thread_id,
            assistant_id="asst_6eb9KdjXtWz5D9a1EFn2MCPD",
        )

        # Letzte Antwort abrufen
        messages = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )
        last_message = messages.data[0].content[0].text.value

        with st.chat_message("assistant"):
            st.markdown(last_message)

        st.session_state.messages.append(
            {"role": "assistant", "content": last_message}
        )
