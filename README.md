# AI Chatbot with Personalities

An interactive chatbot web app built with Streamlit and Groq AI models, featuring personality-based conversations and model selection.

## Features

- 🤖 **Multiple AI Models**: Choose from various Groq models (Llama, Mixtral, Gemma)
- 🎭 **Personality Selection**: 5 different chatbot personalities with specialized knowledge
- 💬 **Real-time Chat**: Interactive chat interface with session memory
- 🔒 **Personality Enforcement**: Chatbots stay within their designated expertise areas
- ☁️ **Free Deployment**: Deploy on Streamlit Cloud for free

## Available Personalities

| Personality | Expertise | Example Topics |
|-------------|-----------|----------------|
| **Math Teacher** | Mathematics, problem-solving | Algebra, calculus, geometry, statistics |
| **Doctor** | Health and medicine | Symptoms, treatments, medical advice |
| **Travel Guide** | Travel and tourism | Destinations, planning, cultural tips |
| **Chef** | Cooking and culinary arts | Recipes, techniques, ingredients |
| **Tech Support** | Technology and IT | Troubleshooting, software, hardware |

## Setup Instructions

### 1. Get a Groq API Key
1. Visit [Groq Console](https://console.groq.com/)
2. Sign up for a free account
3. Generate an API key

### 2. Local Development
1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```

### 3. Deploy to Streamlit Cloud (Free)

1. **Push to GitHub**:
   - Create a new repository on GitHub
   - Push your code to the repository

2. **Deploy on Streamlit Cloud**:
   - Go to [Streamlit Cloud](https://share.streamlit.io/)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository
   - Set the main file path to `app.py`
   - Add your `GROQ_API_KEY` as a secret in the app settings
   - Click "Deploy"

3. **Configure Secrets**:
   - In your Streamlit Cloud app settings
   - Go to "Secrets" tab
   - Add: `GROQ_API_KEY = "your_actual_api_key"`

## Usage

1. **Select AI Model**: Choose from available Groq models in the sidebar
2. **Choose Personality**: Select a chatbot personality that matches your needs
3. **Start Chatting**: Type your message and get personality-specific responses
4. **Clear Conversation**: Use the clear button to start fresh

## Personality Behavior

Each personality is designed to:
- ✅ Answer questions within their expertise area
- ❌ Politely decline questions outside their domain
- 🔄 Redirect users to relevant topics
- 📚 Provide educational and helpful responses

## Technical Details

- **Framework**: Streamlit
- **AI Provider**: Groq Cloud API
- **Models**: Llama 3.1, Mixtral, Gemma
- **Deployment**: Streamlit Cloud (free tier)
- **Session Management**: Built-in Streamlit session state

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your Groq API key is correctly set
2. **Model Not Available**: Some models may have usage limits
3. **Personality Not Working**: Try clearing the conversation and restarting

### Support

- [Groq Documentation](https://console.groq.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Cloud Guide](https://docs.streamlit.io/streamlit-community-cloud)

## License

This project is open source and available under the MIT License.
