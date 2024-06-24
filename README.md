# 🦙 GrumbleChat 💬

GrumbleChat is a Streamlit-based chatbot application that leverages models available in Ollama to provide responses to user inputs. This application allows users to upload PDF files, extract text from them, and use the extracted text to generate responses from selected language models.

## Features

- List and select available models from Ollama.
- Upload PDF files and extract text using `pdfplumber`.
- Generate responses using selected models from Ollama.
- Display chat messages with a user-friendly interface.
- Clear chat history with a single click.

## Installation

1. Clone the repository:

```sh
git clone https://github.com/fzappa/grumble_chat
cd grumble_chat
```

2. Create and activate a virtual environment:

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the required packages:

```sh
pip install -r requirements.txt
```

## Running the Application

1. Ensure the Ollama service is running and accessible at `http://localhost:11434`.

2. Start the Streamlit application:

```sh
streamlit run app.py
```

3. Open your web browser and navigate to `http://localhost:8501` to use the chatbot.

## Usage

1. **Select a Model:**

   - Choose an available model from the dropdown list in the sidebar.

2. **Upload a PDF:**

   - Use the file uploader in the main interface to upload a PDF file.
   - Once uploaded, the text from the PDF will be extracted.

3. **Chat:**

   - The extracted text will be used to generate responses from the selected model.
   - Chat messages will be displayed in the main interface.

4. **Clear Chat History:**
   - Click the "Clear Chat History" button in the sidebar to reset the chat.

## Code Overview

### Constants

- `OLLAMA_API_URL`: The base URL for the Ollama API.
- `DEFAULT_PROMPT`: The default prompt used to initialize the chat.

### Functions

- `list_ollama_models()`: Fetches the list of available models from Ollama.
- `generate_ollama_response(model_name, prompt_input, temperature, top_p, max_length)`: Generates a response using the selected model and input text.
- `build_dialogue()`: Builds the dialogue history from the session state.
- `extract_text_from_pdf(file)`: Extracts text from the uploaded PDF file using `pdfplumber`.

### Sidebar

- Contains elements to select models, adjust parameters, and clear chat history.

### Main Interface

- Displays chat messages and includes a file uploader for PDFs.

## Error Handling

- Provides user-friendly error messages when the Ollama service is not running or connection fails.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.
