import pdfplumber
import requests
import streamlit as st
from langchain_community.llms import Ollama
from PyPDF2 import PdfReader

# Constants
OLLAMA_API_URL = "http://localhost:11434/api"
DEFAULT_PROMPT = "You are a helpful assistant. Please respond in plain text. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."

# Set page configuration
st.set_page_config(page_title="🦙 GrumbleChat 💬")


# Function to list available models in Ollama
def list_ollama_models():
    try:
        response = requests.get(f"{OLLAMA_API_URL}/tags")
        response.raise_for_status()
        data = response.json()
        models = [model["name"] for model in data["models"]]
        return models
    except requests.ConnectionError:
        st.error(
            "Failed to connect to the Ollama service. Please ensure it is running and try again."
        )
        return []
    except requests.RequestException as e:
        st.error(f"Failed to list models: {str(e)}")
        return []


# Function to generate response from Ollama using langchain
def generate_ollama_response(model_name, prompt_input, temperature, top_p, max_length):
    string_dialogue = build_dialogue()
    input_text = f"{string_dialogue}User: {prompt_input}\n\nAssistant: "

    try:
        llm = Ollama(model=model_name)
        response = llm.invoke(
            input_text, temperature=temperature, top_p=top_p, max_length=max_length
        )
        return response
    except Exception as e:
        st.error(f"Failed to generate response: {str(e)}")
        return "Sorry, I couldn't generate a response."


# Helper function to build dialogue history
def build_dialogue():
    dialogue = DEFAULT_PROMPT + "\n\n"
    for message in st.session_state.messages:
        if message["role"] == "user":
            dialogue += f"User: {message['content']}\n\n"
        else:
            dialogue += f"Assistant: {message['content']}\n\n"
    return dialogue


# Function to extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception as e:
        st.error(f"Failed to extract text from PDF: {str(e)}")
    return text


# Sidebar for user inputs
with st.sidebar:
    st.title("🦙 GrumbleChat 💬")
    st.subheader("Models and parameters")
    model_names = list_ollama_models()
    if model_names:
        selected_model = st.selectbox(
            "Choose an Ollama model", model_names, key="selected_model"
        )
        temperature = st.slider("Temperature", 0.01, 1.0, 0.7, 0.01)
        top_p = st.slider("Top_p", 0.01, 1.0, 0.9, 0.01)
        max_length = st.slider("Max_length", 32, 128, 64, 8)
        st.markdown("⚡ Alan Franco ⚡")
    else:
        st.error("No models available in Ollama.")

# Initialize chat messages in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I assist you today?"}
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Clear chat history
def clear_chat_history():
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I assist you today?"}
    ]


st.sidebar.button("Clear Chat History", on_click=clear_chat_history)

# File uploader for PDFs
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

# Process PDF if uploaded
if uploaded_file:
    pdf_text = extract_text_from_pdf(uploaded_file)
    if pdf_text:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": f"Arquivo {uploaded_file.name} carregado com sucesso.",
            }
        )
        with st.chat_message("user"):
            st.write(f"Arquivo {uploaded_file.name} carregado com sucesso.")

        # Generate a new response
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = generate_ollama_response(
                        st.session_state.selected_model,
                        pdf_text,
                        temperature,
                        top_p,
                        max_length,
                    )
                    st.write(f"[{st.session_state.selected_model}]\n\n{response}")
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": f"[{st.session_state.selected_model}]\n\n{response}",
                }
            )
