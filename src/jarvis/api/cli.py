"""Command-line interface for Gemini API"""
from jarvis.api.gemini_client import process_prompt


def main():
    """CLI interface for testing Gemini API"""
    print("JARVIS 3.0 - Gemini API CLI")
    print("Type 'exit' or 'quit' to stop\n")
    
    while True:
        prompt = input("You: ")
        if prompt.lower() in ["exit", "quit"]:
            print("Shutting Down")
            break
        
        response = process_prompt(prompt)
        print(f"CHATBOT: {response}\n")


if __name__ == "__main__":
    main()


