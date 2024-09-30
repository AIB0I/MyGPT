from chatbot import Chatbot
from db import ChatDatabase
from utils import setup_logging
from dotenv import load_dotenv
import os
load_dotenv()
logger = setup_logging()

def main():
    db = ChatDatabase(os.getenv("CHAT_DB"))
    ollama_model = os.getenv("OLLAMA_MODEL")

    logger.info("Starting the chatbot application")

    while True:
        print("\n1. Start a new chat")
        print("2. Continue an existing chat")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            chat_title = input("Enter a title for the new chat: ")
            chat_id = db.create_new_chat(chat_title)
            logger.info(f"Created new chat with ID: {chat_id} and title: {chat_title}")
            chatbot = Chatbot(ollama_model, db, chat_id)
            print(f"Starting new chat with ID: {chat_id}")
            chatbot.chat()
        elif choice == '2':
            chats = db.get_all_chats()
            if not chats:
                logger.info("No existing chats found")
                print("No existing chats found.")
                continue
            print("Existing chats:")
            for chat_id, title in chats:
                print(f"{chat_id}: {title}")
            chat_id = input("Enter the ID of the chat you want to continue: ")
            logger.info(f"User selected to continue chat with ID: {chat_id}")
            chatbot = Chatbot(ollama_model, db, chat_id)
            print(f"Continuing chat with ID: {chat_id}")
            chatbot.chat()
        elif choice == '3':
            logger.info("User chose to exit the application")
            print("Goodbye!")
            break
        else:
            logger.warning(f"Invalid choice entered: {choice}")
            print("Invalid choice. Please try again.")

    db.close()
    logger.info("Application closed")

if __name__ == "__main__":
    main()