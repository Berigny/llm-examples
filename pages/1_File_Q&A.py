import streamlit as st
import openai

# Retrieve the OpenAI API key from Streamlit's secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

with st.sidebar:
    st.markdown("[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/1_File_Q%26A.py)")
    st.markdown("[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)")

st.title("📝 File Q&A with OpenAI")

uploaded_file = st.file_uploader("Upload an article", type=("txt", "md"))

question = st.text_input(
    "Ask something about the article",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question:
    article = uploaded_file.read().decode()
    prompt = f"""Here's an article:\n\n{article}\n\nWhat would you like to ask about this article?\n\n{question}"""

    with st.spinner("Fetching the answer..."):
        try:
            openai.api_key = openai_api_key
            response = openai.Completion.create(
                engine="davinci-codex",  # Change the engine as per your requirement
                prompt=prompt,
                max_tokens=100,
            )
            st.write("### Answer")
            st.write(response.choices[0].text.strip())
        except openai.error.OpenAIError as e:
            st.error(f"OpenAI API error: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
