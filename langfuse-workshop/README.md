# Langfuse Workshop - AI Observability with Flask and OpenAI

This project demonstrates how to integrate Langfuse observability into a Flask application that uses OpenAI's GPT-4 API. You'll learn how to trace AI interactions, monitor performance, and gain insights into your AI application's behavior.

## 🎯 What You'll Learn

- Setting up Langfuse for AI observability
- Integrating OpenAI GPT-4 with Flask
- Tracing and monitoring AI API calls
- Scoring and analyzing AI responses
- Managing environment variables securely

## 🛠️ Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Langfuse account (free at [cloud.langfuse.com](https://cloud.langfuse.com))

## 📁 Project Structure

```
langfuse-workshop/
├── .env                    # Environment variables (API keys)
├── requirements.txt        # Python dependencies
├── src/
│   └── app.py             # Main Flask application
└── README.md              # This file
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Navigate to the project directory
cd langfuse-workshop

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file with your API keys:

```env
# Langfuse Configuration
LANGFUSE_PUBLIC_KEY=pk-lf-your-public-key
LANGFUSE_SECRET_KEY=sk-lf-your-secret-key
LANGFUSE_HOST=https://cloud.langfuse.com

# OpenAI Configuration
OPENAI_API_KEY=sk-proj-your-openai-api-key

# Optional: Flask Configuration
FLASK_DEBUG=true
```

### 3. Run the Application

```bash
python3 src/app.py
```

You should see:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:4000
```

### 4. Test the API

```bash
curl -X POST http://localhost:4000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the capital of France?", "user_id": "test-user"}'
```

Expected response:
```json
{
  "response": "The capital of France is Paris.",
  "trace_id": "f9dd33a47866b0e641faf484abf3424c"
}
```

## 📡 API Endpoints

### POST `/chat`

Send a message to the AI assistant.

**Request Body:**
```json
{
  "message": "Your question here",
  "user_id": "optional-user-identifier"
}
```

**Response:**
```json
{
  "response": "AI assistant's response",
  "trace_id": "unique-trace-identifier"
}
```

**Error Response:**
```json
{
  "error": "Error description"
}
```

## 🔍 Langfuse Observability Features

This application automatically tracks:

- **Traces**: Each chat request creates a unique trace
- **Spans**: OpenAI API calls are tracked as spans within traces
- **Metadata**: Request/response information and model details
- **Scores**: Response length scoring for analysis
- **User Tracking**: Associate requests with specific users

### Viewing Your Data

1. Visit [cloud.langfuse.com](https://cloud.langfuse.com)
2. Log in to your account
3. Navigate to your project dashboard
4. View traces, spans, and analytics

## 🧪 Testing Different Scenarios

Try these example requests:

```bash
# Simple question
curl -X POST http://localhost:4000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain quantum computing in simple terms"}'

# With user tracking
curl -X POST http://localhost:4000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the benefits of renewable energy?", "user_id": "student-123"}'

# Complex query
curl -X POST http://localhost:4000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Write a Python function to calculate fibonacci numbers", "user_id": "developer-456"}'
```

## 📊 Understanding the Traces

In your Langfuse dashboard, you'll see:

- **Trace Overview**: Request timestamp, user ID, and total duration
- **Span Details**: OpenAI API call latency and token usage
- **Input/Output**: Full request and response content
- **Scores**: Custom metrics like response length
- **Metadata**: Model information and API parameters

## 🛡️ Security Best Practices

- Never commit `.env` files to version control
- Use environment variables for all sensitive data
- Rotate API keys regularly
- Monitor API usage and costs
- Implement rate limiting for production use

## 🔧 Troubleshooting

### Common Issues

**Port already in use:**
```bash
lsof -ti:4000 | xargs kill -9
```

**Import errors:**
```bash
pip install -r requirements.txt
```

**API key issues:**
- Verify your keys in the `.env` file
- Check your OpenAI account has available credits
- Ensure your Langfuse project is properly configured

### Debug Mode

Enable detailed logging by setting:
```env
FLASK_DEBUG=true
```

## 📚 Learning Resources

- [Langfuse Documentation](https://langfuse.com/docs)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 🤝 Contributing

This is an educational workshop project. Feel free to:
- Experiment with different AI models
- Add new endpoints and features
- Implement additional Langfuse scoring methods
- Share improvements and learnings

## 📄 License

This project is for educational purposes. Please respect OpenAI's and Langfuse's terms of service.

---

## 🎉 Next Steps

After completing this workshop, consider exploring:

1. **Advanced Langfuse Features**:
   - Custom scoring functions
   - Dataset management
   - A/B testing with different prompts

2. **Production Enhancements**:
   - Rate limiting and authentication
   - Error handling and retry logic
   - Caching and performance optimization

3. **AI Model Experimentation**:
   - Try different OpenAI models (GPT-3.5, GPT-4-turbo)
   - Implement streaming responses
   - Add function calling capabilities

Happy learning! 🚀