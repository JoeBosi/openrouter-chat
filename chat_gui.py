import os
import requests
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from dotenv import load_dotenv
import threading
import time
from datetime import datetime

class OpenRouterChatGUI:
    """
    OpenRouter Chat GUI Application
    
    A graphical user interface for chatting with OpenRouter API using Auto Router model.
    Features long text support, file operations, and conversation management.
    """
    
    def __init__(self, root):
        """Initialize the GUI application with API configuration"""
        self.root = root
        self.root.title("🤖 OpenRouter Chat - Auto Router")
        self.root.geometry("600x700")
        
        # Load environment variables
        load_dotenv()
        
        # Configure API key
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            messagebox.showerror("Error", "API key not found!\nSet OPENROUTER_API_KEY in .env file")
            root.destroy()
            return
        
        # Configure API endpoint
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # Headers for API requests
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/your-repo",
            "X-Title": "Python Chat GUI"
        }
        
        # Auto Router model
        self.model = "auto"
        
        # Conversation history
        self.messages = []
        
        # Limits for handling long texts
        self.max_message_length = 50000  # 50KB per message
        self.max_context_messages = 50   # Maximum messages in context
        
        # Create GUI widgets
        self.create_widgets()
    
    def create_widgets(self):
        """Create the GUI widgets"""
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weight
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🤖 Chat with Auto Router", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Chat area
        self.chat_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=70, height=25, state=tk.DISABLED)
        self.chat_area.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Configure tags for colors
        self.chat_area.tag_config("user", foreground="blue", font=("Arial", 10, "bold"))
        self.chat_area.tag_config("assistant", foreground="green", font=("Arial", 10))
        self.chat_area.tag_config("system", foreground="gray", font=("Arial", 9, "italic"))
        
        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        # Button frame above input
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Paste button
        self.paste_button = ttk.Button(button_frame, text="📋 Paste Text", command=self.paste_text)
        self.paste_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Load file button
        self.file_button = ttk.Button(button_frame, text="📁 Load File", command=self.load_file)
        self.file_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Character count label
        self.char_count_label = ttk.Label(button_frame, text="0/50000 characters")
        self.char_count_label.pack(side=tk.RIGHT)
        
        # Input field
        self.input_var = tk.StringVar()
        self.input_field = ttk.Entry(input_frame, textvariable=self.input_var, font=("Arial", 11))
        self.input_field.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.input_field.bind("<Return>", lambda event: self.send_message())
        self.input_field.bind("<KeyRelease>", self.update_char_count)
        
        # Send button
        self.send_button = ttk.Button(input_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1)
        
        # Control frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Clear button
        self.clear_button = ttk.Button(control_frame, text="🧹 Clear Chat", command=self.clear_chat)
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Export button
        self.export_button = ttk.Button(control_frame, text="💾 Export Chat", command=self.export_chat)
        self.export_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(control_frame, text="Ready", foreground="green")
        self.status_label.pack(side=tk.LEFT)
        
        # Welcome message
        self.add_message("system", "Welcome! I'm your AI assistant with Auto Router. Type a message and press Enter.")
    
    def add_message(self, sender, message):
        """
        Add a message to the chat area
        
        Args:
            sender (str): Message sender ('user', 'assistant', 'system')
            message (str): Message content
        """
        self.chat_area.config(state=tk.NORMAL)
        
        # Timestamp for user/assistant messages
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if sender == "user":
            # Truncate very long messages for display
            display_message = message[:1000] + "..." if len(message) > 1000 else message
            self.chat_area.insert(tk.END, f"[{timestamp}] You: {display_message}\n\n", "user")
        elif sender == "assistant":
            self.chat_area.insert(tk.END, f"[{timestamp}] Assistant: {message}\n\n", "assistant")
        elif sender == "system":
            self.chat_area.insert(tk.END, f"[{timestamp}] {message}\n\n", "system")
        
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
    
    def send_message(self):
        """
        Send a message to the API
        """
        user_message = self.input_var.get().strip()
        
        if not user_message:
            return
        
        # Check message length
        if len(user_message) > self.max_message_length:
            if not messagebox.askyesno("Long Text", 
                f"The text is very long ({len(user_message)} characters).\n"
                f"Do you want to continue? It may take more time."):
                return
        
        # Clear input field
        self.input_var.set("")
        self.update_char_count()
        
        # Disable controls
        self.input_field.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)
        self.paste_button.config(state=tk.DISABLED)
        self.file_button.config(state=tk.DISABLED)
        self.status_label.config(text="Processing...", foreground="orange")
        
        # Add user message
        self.add_message("user", user_message)
        
        # Start request in separate thread
        threading.Thread(target=self.process_message, args=(user_message,), daemon=True).start()
    
    def process_message(self, user_message):
        """
        Process the message in a separate thread
        
        Args:
            user_message (str): The message to process
        """
        try:
            # Context management to prevent overflow
            if len(self.messages) >= self.max_context_messages:
                # Remove old messages keeping the first system message
                system_msgs = [msg for msg in self.messages if msg["role"] == "system"]
                recent_msgs = self.messages[-(self.max_context_messages-1):]
                self.messages = system_msgs + recent_msgs
                self.root.after(0, lambda: self.add_message("system", 
                    f"Context reduced for optimization (max {self.max_context_messages} messages)"))
            
            # Add user message to history
            self.messages.append({"role": "user", "content": user_message})
            
            # Prepare request data
            data = {
                "model": self.model,
                "messages": self.messages
            }
            
            # Longer timeout for long texts
            timeout = 120 if len(user_message) > 10000 else 60
            
            # Make API request
            response = requests.post(self.api_url, headers=self.headers, json=data, timeout=timeout)
            response.raise_for_status()
            
            # Extract response
            result = response.json()
            assistant_message = result['choices'][0]['message']['content']
            
            # Add assistant response to history
            self.messages.append({"role": "assistant", "content": assistant_message})
            
            # Add response to chat
            self.root.after(0, lambda: self.add_message("assistant", assistant_message))
            
        except requests.exceptions.Timeout:
            error_message = "Timeout: The message is too long or the server is slow. Try with shorter text."
            self.root.after(0, lambda: self.add_message("system", error_message))
        except requests.exceptions.RequestException as e:
            error_message = f"Connection error: {e}"
            self.root.after(0, lambda: self.add_message("system", error_message))
        except KeyError as e:
            error_message = f"Response parsing error: {e}"
            self.root.after(0, lambda: self.add_message("system", error_message))
        except Exception as e:
            error_message = f"Unexpected error: {e}"
            self.root.after(0, lambda: self.add_message("system", error_message))
        finally:
            # Re-enable controls
            self.root.after(0, self.enable_controls)
    
    def enable_controls(self):
        """Re-enable the interface controls"""
        self.input_field.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)
        self.paste_button.config(state=tk.NORMAL)
        self.file_button.config(state=tk.NORMAL)
        self.status_label.config(text="Ready", foreground="green")
        self.input_field.focus()
    
    def update_char_count(self, event=None):
        """
        Update the character count display
        
        Args:
            event: Event object (optional)
        """
        text = self.input_var.get()
        char_count = len(text)
        
        # Change color if over limit
        if char_count > self.max_message_length:
            self.char_count_label.config(text=f"{char_count}/{self.max_message_length} ⚠️", foreground="red")
        elif char_count > self.max_message_length * 0.8:
            self.char_count_label.config(text=f"{char_count}/{self.max_message_length}", foreground="orange")
        else:
            self.char_count_label.config(text=f"{char_count}/{self.max_message_length}", foreground="gray")
    
    def paste_text(self):
        """
        Paste text from clipboard
        """
        try:
            clipboard_text = self.root.clipboard_get()
            if clipboard_text:
                current_text = self.input_var.get()
                new_text = current_text + clipboard_text
                
                if len(new_text) > self.max_message_length:
                    if messagebox.askyesno("Text too long", 
                        f"The pasted text exceeds the limit of {self.max_message_length} characters.\n"
                        f"Do you want to truncate it?"):
                        new_text = new_text[:self.max_message_length]
                    else:
                        return
                
                self.input_var.set(new_text)
                self.update_char_count()
                self.add_message("system", f"Text pasted ({len(clipboard_text)} characters)")
        except Exception as e:
            messagebox.showerror("Error", f"Unable to paste text: {e}")
    
    def load_file(self):
        """
        Load text from a file
        """
        file_path = filedialog.askopenfilename(
            title="Select a text file",
            filetypes=[
                ("Text files", "*.txt"),
                ("Markdown files", "*.md"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                if len(content) > self.max_message_length:
                    if messagebox.askyesno("File too long", 
                        f"The file contains {len(content)} characters.\n"
                        f"Do you want to load only the first {self.max_message_length} characters?"):
                        content = content[:self.max_message_length]
                    else:
                        return
                
                self.input_var.set(content)
                self.update_char_count()
                filename = os.path.basename(file_path)
                self.add_message("system", f"File '{filename}' loaded ({len(content)} characters)")
            except Exception as e:
                messagebox.showerror("Error", f"Unable to read file: {e}")
    
    def export_chat(self):
        """
        Export the conversation to a file
        """
        file_path = filedialog.asksaveasfilename(
            title="Save the conversation",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("Markdown files", "*.md"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write("=== OpenRouter Chat - Auto Router ===\n")
                    file.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    file.write("=" * 50 + "\n\n")
                    
                    for msg in self.messages:
                        role = msg['role'].upper()
                        content = msg['content']
                        file.write(f"{role}:\n{content}\n\n")
                        file.write("-" * 30 + "\n\n")
                
                messagebox.showinfo("Success", f"Chat exported to: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Unable to export chat: {e}")
    
    def clear_chat(self):
        """
        Clear the chat history
        """
        self.messages = []
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.delete(1.0, tk.END)
        self.chat_area.config(state=tk.DISABLED)
        self.add_message("system", "Chat cleared. Start a new conversation!")

def main():
    """
    Main function to run the GUI application
    """
    root = tk.Tk()
    app = OpenRouterChatGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
