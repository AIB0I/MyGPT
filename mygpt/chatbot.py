import ollama
from utils import setup_logging

logger = setup_logging()

class Chatbot:
    def __init__(self, ollama_model, chat_db, chat_id=None):
        self.chat_db = chat_db
        self.messages = []
        self.ollama_model = ollama_model
        self.chat_id = chat_id
        logger.info(f"Chatbot initialized with model: {self.ollama_model} and chat database")
        if chat_id:
            self.load_chat_history()

    def send_message(self, user_input):
        logger.info(f"Received user input: {user_input[:50]}...")  # Log first 50 chars of user input
        
        self.messages.append({'role': 'user', 'content': user_input})
        self.chat_db.save_message(self.chat_id, "user", user_input)

        logger.info(f"Querying Ollama with {len(self.messages)} messages")
        response = ollama.chat(model=self.ollama_model, messages=self.messages, stream=False)

        assistant_output = response['message']['content']
        logger.info(f"Received response from Ollama: {assistant_output[:50]}...")  # Log first 50 chars of response

        self.messages.append({'role': 'assistant', 'content': assistant_output})
        self.chat_db.save_message(self.chat_id, "assistant", assistant_output)

        return assistant_output

    def chat(self):
        logger.info("Starting continuous chat")
        print(f"Welcome to chat {self.chat_id}! Type '/exit' to end the conversation.")
        
        while True:
            user_input = input("User: ")
            # print("User:", user_input)
            
            if user_input.lower() == "/exit":
                logger.info("User requested to exit the chat")
                break
            
            assistant_output = self.send_message(user_input)
            print("Assistant:", assistant_output)

    def display_history(self):
        logger.info("Displaying chat history")
        print("\nChat history:")
        for message in self.messages:
            print(f"{message['role']}: {message['content']}")
        print()

    def load_chat_history(self):
        logger.info(f"Loading chat history for chat ID: {self.chat_id}")
        chat_history = self.chat_db.get_chat_history(self.chat_id)
        self.messages = [{"role": role, "content": message} for role, message in chat_history]
        logger.info(f"Loaded {len(self.messages)} messages from chat history")