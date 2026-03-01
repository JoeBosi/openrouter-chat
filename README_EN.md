# OpenRouter Chat - Python

A powerful Python chat application that uses OpenRouter API with Auto Router model for intelligent AI conversations.

## Features

- 🤖 **Auto Router Model**: Automatically selects the best model for each request
- 💬 **Long Text Support**: Handle texts up to 50KB without issues
- 📋 **Clipboard Integration**: Paste long texts directly from clipboard
- 📁 **File Operations**: Load .txt, .md files and export conversations
- 🔄 **Context Management**: Maintains conversation history (max 50 messages)
- 🎨 **Dual Interface**: Both CLI and GUI versions available
- ⚡ **Real-time Character Count**: Visual feedback for message length
- 💾 **Export Functionality**: Save conversations to text/markdown files
- 🛡️ **Error Handling**: Comprehensive error management and timeouts

## Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```

2. Open the `.env` file and insert your OpenRouter API key:
```
OPENROUTER_API_KEY=your_api_key_here
```

To get an API key:
- Go to [OpenRouter.ai](https://openrouter.ai/)
- Sign up or login
- Go to the API Keys section and create a new key

## Usage

### CLI Version
```bash
python chat.py
```

### GUI Version
```bash
python chat_gui.py
```

### Available Commands (CLI)
- `quit` - Exit the chat
- `clear` - Clear conversation history

### GUI Features
- **Paste Text**: 📋 Paste long texts from clipboard
- **Load File**: 📁 Load .txt or .md files
- **Export Chat**: 💾 Save conversation history
- **Clear Chat**: 🧹 Clear conversation history
- **Character Counter**: Real-time character count with visual indicators

## Project Structure

```
├── chat.py              # Main CLI chat application
├── chat_gui.py          # GUI chat application
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── .env                # Your configurations (to create)
├── LICENSE             # MIT License
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## Testing

The application has been thoroughly tested. To run tests:

```bash
# Basic API test
python test_api.py

# GUI test
python test_gui.py

# Complete test suite
python test_complete.py
```

### Test Results ✅

- ✅ **API Connection**: OpenRouter connection working
- ✅ **Model Selection**: Auto Router automatically selects best models
- ✅ **Long Text Handling**: Support for texts up to 50KB
- ✅ **File Operations**: File loading and export functionality
- ✅ **Error Handling**: Comprehensive error management
- ✅ **GUI Components**: All graphical components working
- ✅ **CLI Interface**: Command-line interface operational

## Technical Specifications

- **Max Message Length**: 50,000 characters (50KB)
- **Max Context Messages**: 50 messages in conversation history
- **Timeout**: 60s (normal), 120s (long texts >10KB)
- **Supported File Formats**: .txt, .md for loading; .txt, .md for export
- **Threading**: Non-blocking operations for smooth UI experience

## Notes

- Auto Router model automatically selects the best model for each request
- Conversation history is maintained in memory during the session
- Ensure you have an active internet connection
- For very long texts (>10KB), timeout is automatically extended to 120 seconds

## Author

**Giuseppe Bosi**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please:
1. Check the test results by running `python test_complete.py`
2. Ensure your API key is correctly configured in `.env`
3. Verify internet connection
4. Open an issue with detailed information

---

