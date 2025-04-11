# Rule-Based Chatbot

A modern rule-based chatbot with AI capabilities built using Streamlit and Groq API.

## Features

- Rule-based pattern matching for simple queries
- AI-powered responses for complex questions via Groq API
- Modern glassmorphism UI design with animations
- Dark/light theme toggle
- Responsive layout with cards and custom styled components
- Session history to maintain conversation context

## Demo

![Chatbot Demo](https://example.com/chatbot-demo.gif)

## Installation

1. Clone this repository
   ```
   git clone https://github.com/yourusername/Rule-Based-Chatbot.git
   cd Rule-Based-Chatbot
   ```

2. Install dependencies
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your Groq API key
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Usage

Run the application locally:
```
streamlit run app.py
```

Or deploy to Streamlit Cloud:
1. Push your code to GitHub
2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Add your Groq API key as a secret

## How It Works

The chatbot uses a two-tier approach to handle queries:

1. **Pattern Matching**: For simple queries, it uses predefined regex patterns to match questions and provide answers.
2. **AI Integration**: For complex questions, it leverages the Groq API to generate more sophisticated responses.

## Project Structure

- `app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `packages.txt` - System dependencies for Streamlit Cloud
- `.env` - Environment variables for API keys

## Adding New Rules

Rules are defined in the `init_session_state()` function in `app.py`. Add new rules by following this format:

```python
{
    'patterns': [r'regex_pattern_1', r'regex_pattern_2'],
    'responses': ["Response 1", "Response 2"]
}
```

## Testing

The chatbot includes unit tests to verify functionality:

```
pytest test_chatbot.py
```

## License

MIT 