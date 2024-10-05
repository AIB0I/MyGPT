# MyGPT

MyGPT aims to be a personal assistant designed to learn from user interactions, building a personalized knowledge graph to enhance future conversations. It also generates valuable data for fine-tuning language models for personalization.

## Main Concepts

- **Knowledge Graph**: The chatbot builds a knowledge graph based on user interactions, allowing it to provide more contextually relevant responses over time.
- **Automatic Feedback Loop**: The system collects feedback on its outputs directly through the chat, creating valuable data for fine-tuning and improvement.
- **Personalized Communication**: MyGPT learns the user's preferred tone, structure, and style for specific contexts or types of content.
- **Relationship Dynamics**: Through continued use, the chatbot learns about the user's dynamics with other individuals or entities mentioned in conversations.

## Roadmap for v0.1

For v0.1, we are focusing on establishing core functionality:

- [x] FastAPI backend for handling multiple sessions
- [x] SQLite for interaction data storage
- [x] LiteLLM integration for flexible LLM provider support
- [x] LLM backend to work with Ollama
- [ ] Basic user interface for performing and managing multiple interaction sessions
- [ ] Knowledge graph construction from user interactions
- [ ] Personalization using the knowledge graph

**Note:** This project is under active development. v0.1 aims to provide a functional foundation with basic implementations of key features. Advanced optimizations and more sophisticated implementations of the main concepts will be addressed in future versions.

## Installation and Usage

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Set up your environment variables:
   Create a `.env` file in the `backend` directory with the following content:
   ```
   APP_DB=app.db
   OLLAMA_MODEL=ollama/llama3.2:3b-instruct-q4_K_M
   OLLAMA_API_BASE=http://localhost:11434
   ```
   Adjust the `OLLAMA_MODEL` and `OLLAMA_API_BASE` values if needed.

3. Run the backend server:
   ```
   cd backend
   python -m mygpt.main
   ```

   The FastAPI server will start, and you can interact with it using API calls.

## Project Structure

- `backend/mygpt/main.py`: Main entry point of the application
- `backend/mygpt/api.py`: FastAPI routes and API logic
- `backend/mygpt/db.py`: Database operations for chat history
- `backend/mygpt/session.py`: Session management for chat interactions
- `backend/mygpt/utils.py`: Utility functions (e.g., logging setup)
- `requirements.txt`: List of Python package dependencies

## API Endpoints and Usage Examples

### Start a new chat session or continue an existing one

Endpoint: `POST /session`

Usage:

#### Start a new session
```bash
curl -X POST http://localhost:8000/session \
   -H "Content-Type: application/json" \
   -d '{ "message": "Hello, I would like to start a chat."}'
``` 

The response will include the AI's reply and the newly created session ID:
```json
{
  "response": "Hello! I'm doing well, thank you for asking. How can I assist you today?",
  "session_id": "newly_created_session_id"
}
```

#### Continue an existing session
```bash
curl -X POST http://localhost:8000/session \
  -H "Content-Type: application/json" \
  -d '{"message": "What was our last conversation about?", "session_id": "previously_returned_session_id"}'
```

The response will include the AI's reply and the same session ID:
```json
{
  "response": "Hello! I'm doing well, thank you for asking. How can I assist you today?",
  "session_id": "same_session_id"
}
```

### Retrieve the message history for a specific session

Endpoint: `GET /session/{session_id}/history`

Usage:

```bash
curl http://localhost:8000/session/your_session_id_here/history
```

The response will include the full conversation history for the specified session:

```json
{
  "session_id": "your_session_id_here",
  "history": [
      ["user","Hello, I would like to start a chat."],
      ["assistant","I'd be happy to have a conversation with you. How's your day going so far?"],
      ["user","It's going well, thank you! I'm just exploring this new chatbot technology."],
      ["assistant","That's great! It's always exciting to see new advancements in AI. How can I assist you today?"]
  ]
}
```

## Logging

Logs are stored in the `backend/logs` directory, with each session creating a new log file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
