import openai
import streamlit as st

# Retrieve the OpenAI API key from Streamlit's secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Set the title and caption for the Streamlit app
st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI LLM")

# Initialize session state variable to store the conversation history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display the conversation history
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# Get user input and proceed if the input is not None or empty
if prompt := st.chat_input():
    # Set the OpenAI API key
    openai.api_key = openai_api_key  
    
    # Add user message to session state and display it in the chat
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Show a loading indicator while the bot is fetching a response
    with st.spinner("Assistant is thinking..."):
        try:
            # Call OpenAI API to get a response based on the conversation history
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state["messages"][-20:])
            msg = response.choices[0].message
            
            # Add assistant's response to session state and display it in the chat
            st.session_state["messages"].append(msg)
            st.chat_message("assistant").write(msg.content)
        except openai.error.OpenAIError as e:
            # Handle API errors gracefully
            st.error(f"API error: {e}")
        except Exception as e:
            # Handle other potential errors gracefully
            st.error(f"An unexpected error occurred: {e}")
