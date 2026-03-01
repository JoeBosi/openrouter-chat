# Changelog

All notable changes to OpenRouter Chat will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-01

### Added
- Initial release of OpenRouter Chat application
- CLI chat interface (`chat.py`)
- GUI chat interface (`chat_gui.py`) with Tkinter
- OpenRouter API integration with Auto Router model
- Long text support (up to 50KB per message)
- Conversation history management (max 50 messages)
- File operations:
  - Load text files (.txt, .md)
  - Export conversations to text/markdown
  - Paste text from clipboard
- Real-time character counting with visual indicators
- Context management to prevent overflow
- Dynamic timeout handling (60s normal, 120s for long texts)
- Comprehensive error handling and user feedback
- Threading for non-blocking operations
- Timestamps on all messages
- MIT License
- Complete test suite with 5 test files
- English documentation and code comments
- Git repository with GitHub integration

### Features
- **Auto Router Model Selection**: Automatically selects the best model for each request
- **Dual Interface**: Both command-line and graphical user interfaces
- **Long Text Handling**: Support for texts up to 50KB without crashes
- **File Management**: Load files and export conversations
- **Visual Feedback**: Character count, status indicators, timestamps
- **Error Recovery**: Comprehensive error handling with user-friendly messages
- **Performance**: Optimized for large conversations and texts

### Technical Specifications
- **Max Message Length**: 50,000 characters (50KB)
- **Max Context Messages**: 50 messages in conversation history
- **Timeout**: 60s (normal), 120s (long texts >10KB)
- **Supported File Formats**: .txt, .md for loading; .txt, .md for export
- **Python Version**: 3.7+
- **Dependencies**: requests, python-dotenv, tkinter (built-in)

### Documentation
- Complete README with installation and usage instructions
- API documentation in code comments
- Contributing guidelines
- MIT License
- Test documentation and results

### Testing
- API connection tests
- Long text handling tests
- File operation tests
- GUI component tests
- Error handling tests
- All tests passing (5/5)

---

## Development

### Version History
- **v1.0.0** (2026-03-01): Initial release with full functionality

### Author
- **Giuseppe Bosi** - Initial development and documentation

### License
- **MIT License** - See LICENSE file for details

---

*For more detailed information about changes, see the commit history on GitHub.*
