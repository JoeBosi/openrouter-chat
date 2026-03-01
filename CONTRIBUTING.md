# Contributing to OpenRouter Chat

Thank you for your interest in contributing to OpenRouter Chat! This document provides guidelines and information for contributors.

## How to Contribute

### Reporting Issues

1. Check existing issues to avoid duplicates
2. Use the issue template if available
3. Provide detailed information:
   - Operating system and Python version
   - Steps to reproduce the issue
   - Expected vs actual behavior
   - Error messages or logs

### Making Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes with descriptive messages
6. Push to your fork: `git push origin feature-name`
7. Create a Pull Request

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/your-username/openrouter-chat.git
   cd openrouter-chat
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy environment template:
   ```bash
   cp .env.example .env
   # Add your OpenRouter API key to .env
   ```

5. Run tests:
   ```bash
   python test_complete.py
   ```

## Code Style

- Follow PEP 8 guidelines
- Use English for all comments and documentation
- Add docstrings to all functions and classes
- Use meaningful variable and function names
- Keep functions focused and small

## Testing

Before submitting a pull request:

1. Run the complete test suite:
   ```bash
   python test_complete.py
   ```

2. Test both CLI and GUI versions:
   ```bash
   python chat.py
   python chat_gui.py
   ```

3. Test edge cases:
   - Long text handling
   - File operations
   - Error scenarios

## Pull Request Guidelines

1. Use clear and descriptive titles
2. Describe the changes and their purpose
3. Link to relevant issues
4. Include screenshots for UI changes
5. Ensure all tests pass
6. Update documentation if needed

## Project Structure

```
├── chat.py              # CLI chat application
├── chat_gui.py          # GUI chat application
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── LICENSE             # MIT License
├── README.md           # Project documentation
├── CONTRIBUTING.md     # This file
└── test_*.py           # Test files
```

## Areas for Contribution

- **New Features**: Additional file format support, themes, plugins
- **Performance**: Optimization for large conversations
- **UI/UX**: Improved interface design and user experience
- **Documentation**: Better docs, tutorials, examples
- **Testing**: More comprehensive test coverage
- **Internationalization**: Multi-language support

## Code Review Process

1. All submissions require review
2. Maintain code quality standards
3. Ensure backward compatibility
4. Test thoroughly before merging
5. Update changelog if needed

## Community

- Be respectful and constructive
- Help others with their questions
- Share ideas and suggestions
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to OpenRouter Chat! 🚀
