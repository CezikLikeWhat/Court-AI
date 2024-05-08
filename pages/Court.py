import streamlit as st


class Court:
    def __init__(self):
        self.view()

    def view(self):
        # with st.sidebar:
        #     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        #     st.write("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")

        st.title("Court 💬")
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        # if prompt := st.chat_input():
        #     if not openai_api_key:
        #         st.info("Please add your OpenAI API key to continue.")
        #         st.stop()


simulation = Court()
