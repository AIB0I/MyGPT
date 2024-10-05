from litellm import completion
from .utils import logger

class Session:
    """
    Represents a chat session with the AI model.
    """

    def __init__(self, ollama_model, ollama_api_base, db, session_id):
        """
        Initialize a new session.

        Args:
            ollama_model (str): The name of the Ollama model to use.
            ollama_api_base (str): The base URL for the Ollama API.
            db (DB): Database instance for storing messages.
            session_id (str): Unique identifier for this session.
        """
        self.db = db
        self.messages = []
        self.ollama_model = ollama_model
        self.ollama_api_base = ollama_api_base
        self.session_id = session_id
        logger.info(f"Session initialized with model: {self.ollama_model} and database")
        self.load_session_history()

    def add_message(self, user_input):
        """
        Add a user message to the session and get the AI's response.

        Args:
            user_input (str): The user's input message.

        Returns:
            str: The AI's response to the user's input.

        Raises:
            Exception: If there's an error in the LiteLLM completion.
        """
        logger.info(f"Received user input: {user_input[:50]}...")
        
        # Add user message to the session
        self.messages.append({'role': 'user', 'content': user_input})
        self.db.add_message(self.session_id, "user", user_input)

        logger.info(f"Querying LiteLLM with {len(self.messages)} messages")
        try:
            # Get AI response
            response = completion(
                model=self.ollama_model,
                messages=self.messages,
                api_base=self.ollama_api_base
            )
            assistant_output = response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error in LiteLLM completion: {str(e)}")
            raise

        logger.info(f"Received response from LiteLLM: {assistant_output[:50]}...")

        # Add AI response to the session
        self.messages.append({'role': 'assistant', 'content': assistant_output})
        self.db.add_message(self.session_id, "assistant", assistant_output)

        return assistant_output

    def load_session_history(self):
        """
        Load the session history from the database.
        """
        logger.info(f"Loading session history for session ID: {self.session_id}")
        session_history = self.db.get_session_history(self.session_id)
        self.messages = [{"role": role, "content": message} for role, message in session_history]
        logger.info(f"Loaded {len(self.messages)} messages from session history")