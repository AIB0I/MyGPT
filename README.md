# MyGPT

MyGPT aims to be a personal assistant designed to learn from user interactions, building a personalized knowledge graph to enhance future conversations. It also generates valuable data for fine-tuning the language models for pesonalization.

## Main Concepts

- **Knowledge Graph**: The chatbot builds a knowledge graph based on user interactions, allowing it to provide more contextually relevant responses over time.
- **Automatic Feedback Loop**: The system collects feedback on its outputs directly through the chat, creating valuable data for fine-tuning and improvement.
- **Personalized Communication**: MyGPT learns the user's preferred tone, structure, and style for specific contexts or types of content.
- **Relationship Dynamics**: Through continued use, the chatbot learns about the user's dynamics with other individuals or entities mentioned in conversations.

## Features

- [x] Start new chat sessions
- [x] Continue existing chat sessions
- [x] Chat history persistence
- [x] Support for Ollama (with plans to support other LLM providers in the future)
- [x] Configurable Ollama model
- [x] SQLite for chat data storage (with plans to support more robust databases in the future)
- [ ] Knowledge graph construction from user interactions
- [ ] Knowledge graph retrival
- [ ] Automatic feedback collection from user interactions
- [ ] UI

**Note:** This project is under active development. While it aims to provide advanced personalization and learning capabilities, some features may still be in progress or experimental.

## Installation and Usage

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/mygpt.git
   cd mygpt
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   Create a `.env` file in the `mygpt` directory with the following content:
   ```
   CHAT_DB=chat_history.db
   OLLAMA_MODEL=llama3.2:3b-instruct-q4_K_M
   ```
   Adjust the `OLLAMA_MODEL` value if you want to use a different model.

4. Run the main script:
   ```
   python mygpt/main.py
   ```

   Follow the prompts to start a new chat or continue an existing one. As you interact with MyGPT, it will continuously learn and adapt to your communication style and needs.

## Project Structure

- `mygpt/main.py`: Main entry point of the application
- `mygpt/chatbot.py`: Chatbot class implementation
- `mygpt/db.py`: Database operations for chat history
- `mygpt/utils.py`: Utility functions (e.g., logging setup)
- `requirements.txt`: List of Python package dependencies

## Logging

Logs are stored in the `logs` directory, with each session creating a new log file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
