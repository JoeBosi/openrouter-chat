import os
import requests
import json
from dotenv import load_dotenv

class OpenRouterChat:
    """
    OpenRouter Chat CLI Application
    
    A command-line interface for chatting with OpenRouter API using Auto Router model.
    Supports long text handling and conversation history management.
    """
    
    def __init__(self):
        """Initialize the chat application with API configuration"""
        # Load environment variables
        load_dotenv()
        
        # Configure API key
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("API key not found! Set OPENROUTER_API_KEY in .env file")
        
        # Configure API endpoint
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # Headers for API requests
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/your-repo",  # Optional: replace with your site
            "X-Title": "Python Chat App"  # Optional: your app name
        }
        
        # Auto Router model
        self.model = "auto"
        
        # Conversation history
        self.messages = []
    
    def send_message(self, user_message):
        """
        Send a message to the API and get the response
        
        Args:
            user_message (str): The message to send
            
        Returns:
            str: The assistant's response or error message
        """
        # Add user message to history
        self.messages.append({"role": "user", "content": user_message})
        
        # Prepare request data
        data = {
            "model": self.model,
            "messages": self.messages
        }
        
        try:
            # Make API request
            response = requests.post(self.api_url, headers=self.headers, json=data)
            response.raise_for_status()
            
            # Extract response
            result = response.json()
            assistant_message = result['choices'][0]['message']['content']
            
            # Add assistant response to history
            self.messages.append({"role": "assistant", "content": assistant_message})
            
            return assistant_message
            
        except requests.exceptions.RequestException as e:
            return f"Connection error: {e}"
        except KeyError as e:
            return f"Response parsing error: {e}"
        except Exception as e:
            return f"Unexpected error: {e}"
    
    def clear_history(self):
        """Clear the conversation history"""
        self.messages = []
    
    def get_conversation_history(self):
        """
        Get the complete conversation history
        
        Returns:
            list: List of message dictionaries
        """
        return self.messages

def main():
    """
    Main function to run the chat application
    """
    print("🤖 OpenRouter Chat - Auto Router Model")
    print("=" * 50)
    print("Type 'quit' to exit, 'clear' to clear history")
    print("=" * 50)
    
    try:
        # Initialize chat
        chat = OpenRouterChat()
        print("✅ Chat initialized successfully!")
        print()
        
        while True:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check special commands
            if user_input.lower() == 'quit':
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'clear':
                chat.clear_history()
                print("🧹 History cleared!")
                continue
            elif not user_input:
                continue
            
            # Send message and get response
            print("🤖 Auto Router is thinking...")
            response = chat.send_message(user_input)
            print(f"Assistant: {response}")
            print()
    
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Make sure you created a .env file with your OpenRouter API key")
    except KeyboardInterrupt:
        print("\n👋 Chat interrupted. Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
