# Contributing to Darkflobi

First off, thanks for taking the time to contribute! 🎉

## Code of Conduct

This project and everyone participating in it is governed by our commitment to creating a welcoming environment. Please be respectful and constructive in all interactions.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (code snippets, screenshots)
- **Describe the behavior you observed and expected**
- **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the proposed feature**
- **Explain why this enhancement would be useful**
- **List any alternatives you've considered**

### Pull Requests

1. **Fork the repo** and create your branch from `main`
2. **Follow the coding style** of the project
3. **Add tests** if applicable
4. **Update documentation** as needed
5. **Ensure all tests pass**
6. **Write a clear PR description**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/darkflobi-automation.git
cd darkflobi-automation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest
```

## Style Guide

- **Python:** Follow PEP 8, use Black for formatting
- **Commits:** Use clear, descriptive commit messages
- **Documentation:** Keep docs up to date with changes

## Project Structure

```
darkflobi-automation/
├── moltbook-integration/    # Moltbook API
├── prediction-markets/      # Market logic
├── social-media/           # Social posting
├── twitter-automation/     # Twitter API
├── voice-integration/      # Voice synthesis
└── skills/                 # Skill modules
```

## Questions?

Feel free to open an issue or reach out on [Twitter](https://twitter.com/darkflobi).

---

Thank you for contributing! 😁
