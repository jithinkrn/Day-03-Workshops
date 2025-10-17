# LLM Token Monitor

This project demonstrates how to monitor LLM token usage using FastAPI, Prometheus, and Grafana.

## Project Structure

```
llm-token-monitor/
├── app/
│   └── main.py                 # FastAPI app with token metrics
├── docker-compose.yml          # Docker orchestration  
├── prometheus.yml              # Prometheus config
├── requirements.txt            # Python dependencies
├── Dockerfile                  # FastAPI containerization
├── .env                        # Environment variables (create from .env.example)
├── .env.example               # Environment template
└── grafana/
    ├── dashboards/
    │   ├── llm-dashboard.json  # Grafana dashboard
    │   └── dashboard.yml       # Dashboard provisioning
    └── datasources/
        └── prometheus.yml      # Datasource provisioning
```

## Prerequisites

1. **Docker and Docker Compose** installed
2. **OpenAI API key** from https://platform.openai.com/account/api-keys
3. **Conda environment** (optional for local development)

## Setup Instructions

### 1. Set Environment Variables

Create a `.env` file in the project root:

```bash
echo "OPENAI_API_KEY=your-actual-openai-api-key" > .env
```

**Important**: Replace `your-actual-openai-api-key` with your real OpenAI API key that starts with `sk-`

### 2. Start the Services

```bash
docker-compose up --build
```

This will automatically:
- Build the FastAPI app with the latest code
- Start all services with proper networking
- Load your API key from the `.env` file

This will start:
- **FastAPI app** on http://localhost:8000
- **Prometheus** on http://localhost:9090  
- **Grafana** on http://localhost:3000

### 3. Access the Services

- **FastAPI Documentation**: http://localhost:8000/docs
- **Prometheus Dashboard**: http://localhost:9090
- **Grafana Dashboard**: http://localhost:3000 (admin/admin)

### 4. Verify Setup

Check if all services are running:
```bash
docker-compose ps
```

You should see all containers in "Up" status.

## Usage

### Send a Chat Request

Test the API using curl:
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Hello! How are you?", "model": "gpt-3.5-turbo"}'
```

Or use the interactive documentation at http://localhost:8000/docs:
1. Click on "POST /chat"  
2. Click "Try it out"
3. Enter your prompt and model
4. Click "Execute"

### View Metrics

- **Raw Prometheus metrics**: http://localhost:8000/metrics
- **Prometheus query interface**: http://localhost:9090
- **Grafana dashboard**: http://localhost:3000 (admin/admin)

### Monitor Token Usage

After sending a few chat requests, you can monitor:
- Total tokens used per model
- Prompt vs completion token distribution  
- Request rate and usage patterns

## Metrics Available

- `llm_tokens_total`: Total tokens used by model
- `llm_tokens_prompt`: Prompt tokens used by model
- `llm_tokens_completion`: Completion tokens used by model

## Development

### Local Development (without Docker)

To run the FastAPI app locally for development:

```bash
# Activate conda environment
conda activate aaspy312_d3

# Install dependencies (automatically installs compatible versions)
pip install fastapi uvicorn openai prometheus_client python-dotenv

# Set your OpenAI API key in .env file (recommended)
echo "OPENAI_API_KEY=your-api-key" > .env

# Or set as environment variable
export OPENAI_API_KEY="your-api-key"

# Run the app
cd app
uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

The app will be available at http://localhost:8002

### Updating Dependencies

If you modify dependencies:
```bash
# Generate new requirements from conda environment
conda activate aaspy312_d3
pip freeze | grep -E "(fastapi|uvicorn|openai|prometheus|pydantic|python-dotenv)" > requirements.txt

# Rebuild Docker containers
docker-compose down
docker-compose up --build
```

## Troubleshooting

### Common Issues

1. **OpenAI API errors**:
   - Make sure your API key is valid and has sufficient credits
   - Verify the API key starts with `sk-` and is correctly set in `.env`
   - Check the terminal output for "API Key loaded: sk-proj-..." confirmation

2. **Docker issues**:
   - Ensure Docker is running and ports 3000, 8000, 9090 are not in use
   - Use `docker-compose down` to stop containers before rebuilding
   - Check container logs: `docker-compose logs fastapi-app`

3. **Grafana dashboard not loading**:
   - Wait ~30 seconds after starting for all services to initialize
   - Check that Prometheus is accessible at http://localhost:9090
   - Verify datasource is configured correctly in Grafana

4. **Package dependency conflicts**:
   - Use the provided `requirements.txt` (generated from working conda environment)
   - Avoid mixing pip and conda installs in the same environment

### Checking Service Status

```bash
# Check all containers
docker-compose ps

# View logs
docker-compose logs

# View specific service logs  
docker-compose logs fastapi-app
docker-compose logs prometheus
docker-compose logs grafana
```

### Port Conflicts

If ports are already in use, you can modify `docker-compose.yml`:
```yaml
services:
  fastapi-app:
    ports:
      - "8001:8000"  # Use different external port
```