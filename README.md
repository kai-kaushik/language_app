# Language Translator Assistant

A simple web app for translating text between multiple languages with different politeness levels. Built with Python using Reflex framework and OpenAI's API.

## Features

- **Multi-language support**: English, Japanese, French, Hindi, Mandarin Chinese
- **Politeness levels**: From casual to super polite translations
- **Japanese specialization**: Includes Kanji, Romanji, and word definitions for N4+ level words
- **Responsive design**: Works on desktop and mobile
- **Dark mode toggle**

## Tech Stack

- **Backend**: Python with Reflex framework
- **AI**: OpenAI GPT-3.5-turbo API
- **Frontend**: Reflex (pure Python)
- **Deployment**: Railway

## Quick Setup

### Prerequisites
- Python 3.11+
- OpenAI API key

### Local Development

1. Clone and install dependencies:
```bash
git clone <your-repo-url>
cd language_app
pip install -r requirements.txt
```

2. Set environment variable:
```bash
export OPENAI_KEY="your-openai-api-key"
```

3. Run the app:
```bash
reflex run
```

Visit `http://localhost:3000`

## Deploy to Railway

1. Connect your GitHub repo to Railway
2. Set environment variable: `OPENAI_KEY=your-api-key`
3. Deploy!

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_KEY` | Your OpenAI API key | Yes |

## Project Structure

```
language_app/
├── language_app/
│   ├── __init__.py
│   └── language_app.py      # Main app logic
├── assets/                  # Static files
├── rxconfig.py             # Reflex configuration
├── requirements.txt        # Python dependencies
└── README.md
```

## Usage

1. Select input and output languages
2. Choose politeness level
3. Enter text to translate
4. Add optional instructions if needed
5. Click "Translate"

---

Made with ❤️ by Kai Kaushik