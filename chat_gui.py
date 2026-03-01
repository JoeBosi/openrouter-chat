import os
import requests
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from dotenv import load_dotenv
import threading
import time
from datetime import datetime
import markdown2
from tkhtmlview import HTMLLabel

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
        self.root.geometry("700x900")
        
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
        
        # Track current system instructions to avoid duplication
        self.current_system_prompt = ""
        
        # Limits for handling long texts
        self.max_message_length = 50000  # 50KB per message
        self.max_context_messages = 50   # Maximum messages in context
        
        # Additional instructions for better prompts
        self.additional_instructions = {
            'length': 'medium',  # short, medium, long
            'tone': 'professional',  # casual, professional, formal, friendly
            'style': 'detailed',  # concise, detailed, creative, technical
            'format': 'paragraph',  # paragraph, bullet_points, numbered_list
            'custom': ''  # Custom instructions
        }
        
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
        
        # Chat area with markdown support
        self.chat_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=70, height=25, state=tk.DISABLED)
        self.chat_area.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Configure tags for different message types and markdown elements
        self.chat_area.tag_config("user", foreground="#0066cc", font=("Arial", 10, "bold"))
        self.chat_area.tag_config("assistant", foreground="#009900", font=("Arial", 10))
        self.chat_area.tag_config("system", foreground="#666666", font=("Arial", 9, "italic"))
        
        # Markdown formatting tags
        self.chat_area.tag_config("heading1", font=("Arial", 14, "bold"))
        self.chat_area.tag_config("heading2", font=("Arial", 13, "bold"))
        self.chat_area.tag_config("heading3", font=("Arial", 12, "bold"))
        self.chat_area.tag_config("bold", font=("Arial", 10, "bold"))
        self.chat_area.tag_config("italic", font=("Arial", 10, "italic"))
        self.chat_area.tag_config("code", font=("Consolas", 10), background="#f0f0f0")
        self.chat_area.tag_config("pre", font=("Consolas", 9), background="#f8f8f8", lmargin1=20, lmargin2=20)
        
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
        
        # Main input area
        self.input_text = scrolledtext.ScrolledText(input_frame, width=70, height=4, wrap=tk.WORD, font=("Arial", 11))
        self.input_text.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.input_text.bind("<Control-Return>", lambda event: self.send_message())
        self.input_text.bind("<KeyRelease>", self.update_char_count)
        
        # Send button
        self.send_button = ttk.Button(input_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1)
        
        # Configuration frame
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        config_frame.columnconfigure(1, weight=1)
        
        # API Key field
        ttk.Label(config_frame, text="API Key:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.api_key_var = tk.StringVar()
        self.api_key_entry = ttk.Entry(config_frame, textvariable=self.api_key_var, show="*", width=50)
        self.api_key_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Load API key from .env if exists
        if self.api_key:
            self.api_key_var.set("*" * 20)  # Show masked version
        
        # Update API key button
        self.update_key_button = ttk.Button(config_frame, text="Update Key", command=self.update_api_key)
        self.update_key_button.grid(row=0, column=2, padx=(5, 0), pady=(0, 5))
        
        # Additional instructions frame
        instructions_frame = ttk.LabelFrame(main_frame, text="Response Instructions", padding="10")
        instructions_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        instructions_frame.columnconfigure(1, weight=1)
        
        # Length selection
        ttk.Label(instructions_frame, text="Length:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.length_var = tk.StringVar(value=self.additional_instructions['length'])
        length_combo = ttk.Combobox(instructions_frame, textvariable=self.length_var, 
                                   values=["short", "medium", "long"], state="readonly", width=15)
        length_combo.grid(row=0, column=1, sticky=tk.W, pady=(0, 5))
        
        # Tone selection
        ttk.Label(instructions_frame, text="Tone:").grid(row=0, column=2, sticky=tk.W, padx=(20, 0), pady=(0, 5))
        self.tone_var = tk.StringVar(value=self.additional_instructions['tone'])
        tone_combo = ttk.Combobox(instructions_frame, textvariable=self.tone_var,
                                 values=["casual", "professional", "formal", "friendly"], state="readonly", width=15)
        tone_combo.grid(row=0, column=3, sticky=tk.W, padx=(20, 0), pady=(0, 5))
        
        # Style selection
        ttk.Label(instructions_frame, text="Style:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.style_var = tk.StringVar(value='detailed')
        style_combo = ttk.Combobox(instructions_frame, textvariable=self.style_var,
                                   values=["concise", "detailed", "creative", "technical"], state="readonly", width=15)
        style_combo.grid(row=1, column=1, sticky=tk.W, pady=(0, 5))
        
        # Format selection
        ttk.Label(instructions_frame, text="Format:").grid(row=1, column=2, sticky=tk.W, padx=(20, 0), pady=(0, 5))
        self.format_var = tk.StringVar(value=self.additional_instructions['format'])
        format_combo = ttk.Combobox(instructions_frame, textvariable=self.format_var,
                                   values=["paragraph", "bullet_points", "numbered_list"], state="readonly", width=15)
        format_combo.grid(row=1, column=3, sticky=tk.W, padx=(20, 0), pady=(0, 5))
        
        # Custom instructions
        ttk.Label(instructions_frame, text="Custom Instructions:").grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.custom_text = scrolledtext.ScrolledText(instructions_frame, width=70, height=5, wrap=tk.WORD)
        self.custom_text.grid(row=2, column=1, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        self.custom_text.insert(tk.END, self.additional_instructions['custom'])
        
        # Update instructions button
        self.update_instructions_button = ttk.Button(instructions_frame, text="Apply Instructions", 
                                                   command=self.update_instructions)
        self.update_instructions_button.grid(row=3, column=0, columnspan=4, pady=(10, 0))
        
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
        self.add_message("system", "Welcome! I'm your AI assistant with Auto Router. Configure your settings below and start chatting!")
    
    def render_markdown(self, text):
        """
        Render markdown text with formatting tags
        
        Args:
            text (str): Markdown text to render
        """
        import re
        
        # Store original text for processing
        rendered_text = text
        
        # Headers
        rendered_text = re.sub(r'^# (.+)$', r'\1', rendered_text, flags=re.MULTILINE)
        rendered_text = re.sub(r'^## (.+)$', r'\1', rendered_text, flags=re.MULTILINE)
        rendered_text = re.sub(r'^### (.+)$', r'\1', rendered_text, flags=re.MULTILINE)
        
        # Bold text
        rendered_text = re.sub(r'\*\*(.+?)\*\*', r'\1', rendered_text)
        
        # Italic text
        rendered_text = re.sub(r'\*(.+?)\*', r'\1', rendered_text)
        
        # Inline code
        rendered_text = re.sub(r'`(.+?)`', r'\1', rendered_text)
        
        # Code blocks
        rendered_text = re.sub(r'```(.+?)```', r'\1', rendered_text, flags=re.DOTALL)
        
        return rendered_text
    
    def add_message(self, sender, message):
        """
        Add a message to the chat area with markdown rendering
        
        Args:
            sender (str): Message sender (user, assistant, system)
            message (str): Message content
        """
        timestamp = datetime.now().strftime("%H:%M")
        
        self.chat_area.config(state=tk.NORMAL)
        
        if sender == "user":
            # User messages are plain text
            self.chat_area.insert(tk.END, f"[{timestamp}] You: {message}\n\n", "user")
        elif sender == "assistant":
            # Assistant messages are rendered with markdown
            self.chat_area.insert(tk.END, f"[{timestamp}] Assistant:\n", "assistant")
            
            # Process markdown line by line
            lines = message.split('\n')
            for line in lines:
                if line.startswith('# '):
                    self.chat_area.insert(tk.END, line[2:] + '\n', "heading1")
                elif line.startswith('## '):
                    self.chat_area.insert(tk.END, line[3:] + '\n', "heading2")
                elif line.startswith('### '):
                    self.chat_area.insert(tk.END, line[4:] + '\n', "heading3")
                elif line.startswith('```'):
                    # Code block
                    if line == '```':
                        self.chat_area.insert(tk.END, '\n', "pre")
                    else:
                        self.chat_area.insert(tk.END, line + '\n', "pre")
                elif line.strip().startswith('- '):
                    # Bullet point
                    self.chat_area.insert(tk.END, '  • ' + line[2:] + '\n', "assistant")
                elif line.strip().startswith('1. '):
                    # Numbered list
                    self.chat_area.insert(tk.END, '  ' + line + '\n', "assistant")
                else:
                    # Regular text with inline formatting
                    processed_line = self.render_markdown(line)
                    self.chat_area.insert(tk.END, processed_line + '\n', "assistant")
            
            self.chat_area.insert(tk.END, '\n')
        elif sender == "system":
            # System messages are plain text with different style
            self.chat_area.insert(tk.END, f"[{timestamp}] {message}\n\n", "system")
        
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
    
    def send_message(self):
        """
        Send a message to the API
        """
        user_message = self.input_text.get("1.0", tk.END).strip()
        
        if not user_message:
            return
        
        # Check message length
        if len(user_message) > self.max_message_length:
            if not messagebox.askyesno("Long Text", 
                f"The text is very long ({len(user_message)} characters).\n"
                f"Do you want to continue? It may take more time."):
                return
        
        # Clear input field
        self.input_text.delete("1.0", tk.END)
        self.update_char_count()
        
        # Disable controls
        self.input_text.config(state=tk.DISABLED)
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
            
            # Build current system prompt
            system_prompt = self.build_system_prompt()
            
            # Remove old system message if it exists and instructions changed
            if self.messages and self.messages[0]["role"] == "system":
                if system_prompt != self.current_system_prompt:
                    # Instructions changed, remove old system message
                    self.messages = self.messages[1:]
                    self.current_system_prompt = system_prompt
            
            # Add system message if we have instructions and no system message exists
            if system_prompt and (not self.messages or self.messages[0]["role"] != "system"):
                self.messages.insert(0, {"role": "system", "content": system_prompt})
                self.current_system_prompt = system_prompt
            
            # Add user message to history
            user_msg = {"role": "user", "content": user_message}
            self.messages.append(user_msg)
            
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
    
    def update_api_key(self):
        """
        Update the API key from the input field
        """
        new_key = self.api_key_var.get().strip()
        
        if not new_key:
            messagebox.showerror("Error", "Please enter an API key")
            return
        
        # Check if it's masked (already set)
        if new_key.startswith("*"):
            messagebox.showinfo("Info", "API key is already set. Enter a new key to update.")
            return
        
        # Update the API key
        self.api_key = new_key
        self.headers["Authorization"] = f"Bearer {self.api_key}"
        
        # Mask the display
        self.api_key_var.set("*" * min(len(new_key), 20))
        
        # Save to .env file
        try:
            with open('.env', 'w') as f:
                f.write(f"OPENROUTER_API_KEY={new_key}\n")
            messagebox.showinfo("Success", "API key updated successfully!")
            self.add_message("system", "API key updated and saved to .env file")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save API key: {e}")
    
    def update_instructions(self):
        """
        Update additional instructions from the GUI fields
        """
        old_instructions = self.additional_instructions.copy()
        
        self.additional_instructions['length'] = self.length_var.get()
        self.additional_instructions['tone'] = self.tone_var.get()
        self.additional_instructions['style'] = self.style_var.get()
        self.additional_instructions['format'] = self.format_var.get()
        self.additional_instructions['custom'] = self.custom_text.get("1.0", tk.END).strip()
        
        # Check if instructions actually changed
        if old_instructions != self.additional_instructions:
            # Reset system prompt tracking to force update
            self.current_system_prompt = ""
            
            # Remove existing system message from conversation
            if self.messages and self.messages[0]["role"] == "system":
                self.messages = self.messages[1:]
            
            messagebox.showinfo("Success", "Response instructions updated!\nNew instructions will apply to next messages.")
            self.add_message("system", f"Instructions updated: {self.get_instruction_summary()}")
        else:
            messagebox.showinfo("Info", "Instructions unchanged.")
    
    def get_instruction_summary(self):
        """
        Get a summary of current instructions
        
        Returns:
            str: Summary of instructions
        """
        parts = []
        if self.additional_instructions['length'] != 'medium':
            parts.append(f"length: {self.additional_instructions['length']}")
        if self.additional_instructions['tone'] != 'professional':
            parts.append(f"tone: {self.additional_instructions['tone']}")
        if self.additional_instructions['style'] != 'clear':
            parts.append(f"style: {self.additional_instructions['style']}")
        if self.additional_instructions['format'] != 'paragraph':
            parts.append(f"format: {self.additional_instructions['format']}")
        if self.additional_instructions['custom']:
            parts.append(f"custom: {self.additional_instructions['custom'][:50]}...")
        
        return ", ".join(parts) if parts else "default settings"
    
    def build_system_prompt(self):
        """
        Build a system prompt based on additional instructions
        
        Returns:
            str: System prompt with instructions
        """
        instructions = []
        
        # Always include markdown formatting instruction
        instructions.append("Always format your responses using Markdown syntax with proper headings, bold, italic, code blocks, lists, and other formatting elements.")
        
        # Length instructions
        length_map = {
            'short': 'Keep your response concise and brief, under 100 words.',
            'medium': 'Provide a balanced response with moderate detail, 100-300 words.',
            'long': 'Give a comprehensive and detailed response, over 300 words.'
        }
        if self.additional_instructions['length'] in length_map:
            instructions.append(length_map[self.additional_instructions['length']])
        
        # Tone instructions
        tone_map = {
            'casual': 'Use a friendly, informal tone like talking to a friend.',
            'professional': 'Maintain a professional, business-like tone.',
            'formal': 'Use a formal, respectful tone with proper etiquette.',
            'friendly': 'Be warm, approachable, and encouraging.'
        }
        if self.additional_instructions['tone'] in tone_map:
            instructions.append(tone_map[self.additional_instructions['tone']])
        
        # Style instructions
        style_map = {
            'concise': 'Be direct and to the point, avoid unnecessary words.',
            'detailed': 'Provide thorough explanations with examples.',
            'creative': 'Use creative language, metaphors, and engaging descriptions.',
            'technical': 'Use precise technical terminology and structured explanations.'
        }
        if self.additional_instructions['style'] in style_map:
            instructions.append(style_map[self.additional_instructions['style']])
        
        # Format instructions
        format_map = {
            'paragraph': 'Format your response as well-structured paragraphs.',
            'bullet_points': 'Use bullet points for key information and lists.',
            'numbered_list': 'Use numbered lists for sequential information.'
        }
        if self.additional_instructions['format'] in format_map:
            instructions.append(format_map[self.additional_instructions['format']])
        
        # Custom instructions
        if self.additional_instructions['custom']:
            instructions.append(f"Additional requirements: {self.additional_instructions['custom']}")
        
        return " ".join(instructions) if instructions else ""
    
    def enable_controls(self):
        """Re-enable the interface controls"""
        self.input_text.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)
        self.paste_button.config(state=tk.NORMAL)
        self.file_button.config(state=tk.NORMAL)
        self.status_label.config(text="Ready", foreground="green")
        self.input_text.focus()
    
    def update_char_count(self, event=None):
        """
        Update the character count display
        
        Args:
            event: Event object (optional)
        """
        text = self.input_text.get("1.0", tk.END)
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
                current_text = self.input_text.get("1.0", tk.END)
                new_text = current_text + clipboard_text
                
                if len(new_text) > self.max_message_length:
                    if messagebox.askyesno("Text too long", 
                        f"The pasted text exceeds the limit of {self.max_message_length} characters.\n"
                        f"Do you want to truncate it?"):
                        new_text = new_text[:self.max_message_length]
                    else:
                        return
                
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert(tk.END, new_text)
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
                
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert(tk.END, content)
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
        """Clear the chat history"""
        if messagebox.askyesno("Clear Chat", "Are you sure you want to clear the entire conversation?"):
            self.messages = []
            self.current_system_prompt = ""
            self.chat_area.config(state=tk.NORMAL)
            self.chat_area.delete("1.0", tk.END)
            self.chat_area.config(state=tk.DISABLED)
            self.add_message("system", "Chat cleared. Ready for a new conversation!")

def main():
    """
    Main function to run the GUI application
    """
    root = tk.Tk()
    app = OpenRouterChatGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
