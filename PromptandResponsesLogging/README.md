# ELK Stack for LLM Logging and Monitoring

This project provides a complete ELK (Elasticsearch, Logstash, Kibana) stack setup for logging and monitoring Large Language Model (LLM) prompts and responses. It includes comprehensive logging utilities, analytics capabilities, and visualization dashboards.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   LLM App       │    │    Logstash     │    │ Elasticsearch   │    │     Kibana      │
│                 │───▶│                 │───▶│                 │───▶│                 │
│ Python Logger   │    │ Log Processing  │    │  Data Storage   │    │  Visualization  │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.7+
- 4GB+ available RAM

### 1. Start the ELK Stack

```bash
# Clone or navigate to the project directory
cd PromptandResponsesLogging

# Start all services
docker-compose up -d

# Check service status
docker-compose ps
```

### 2. Generate Sample Data

```bash
# Run the example application to generate sample logs
python example_app.py
```

### 3. Access Kibana

1. Open your browser and go to: http://localhost:5601
2. Wait for Kibana to fully load (may take 2-3 minutes)

### 4. Create Data View (Index Pattern)

1. Go to **Stack Management** → **Kibana** → **Data Views**
2. Click **Create data view**
3. Enter name: `LLM Logs`
4. Enter index pattern: `llm-logs-*`
5. Select `timestamp` as the timestamp field
6. Click **Save data view to Kibana**

### 5. Explore Your Data

1. Go to **Discover** to see your logs
2. Go to **Visualize** or **Dashboard** to create charts

## 📊 Dashboard Setup

### Recommended Visualizations

#### 1. Token Usage Over Time
- **Type**: Line chart
- **X-axis**: `timestamp` (Date histogram)
- **Y-axis**: `tokens_used` (Average)

#### 2. Response Latency Distribution
- **Type**: Histogram
- **Field**: `latency_ms`
- **Interval**: 50

#### 3. Most Active Users
- **Type**: Pie chart or Data table
- **Field**: `user_id.keyword` (Terms aggregation)

#### 4. Prompt Categories
- **Type**: Pie chart
- **Field**: `prompt_category.keyword` (Terms aggregation)

#### 5. Hourly Activity Pattern
- **Type**: Vertical bar chart
- **X-axis**: `hour_of_day` (Terms)
- **Y-axis**: Count

#### 6. Model Performance Comparison
- **Type**: Data table
- **Rows**: `model.keyword`
- **Metrics**: 
  - Average `latency_ms`
  - Average `tokens_used`
  - Count

### Creating Visualizations

1. Go to **Visualize** → **Create visualization**
2. Choose visualization type
3. Select `LLM Logs` data view (or `llm-logs-*` index pattern)
4. Configure as described above
5. Save your visualization

### Creating Dashboard

1. Go to **Dashboard** → **Create dashboard**
2. Click **Add** and select your visualizations
3. Arrange and resize as needed
4. Save your dashboard

## 📁 Project Structure

```
PromptandResponsesLogging/
├── docker-compose.yml          # ELK stack configuration
├── logstash.conf              # Logstash pipeline configuration
├── llm_logger.py              # Python logging utilities
├── example_app.py             # Example LLM application
├── logs/                      # Log files directory
│   └── llm_logs.json         # Generated log files
├── security/                  # Production security configurations
│   ├── docker-compose-secure.yml
│   └── elasticsearch.yml
└── README.md                  # This file
```

## 🐍 Python Integration

### Basic Usage

```python
from llm_logger import LLMLogger

logger = LLMLogger()

# Log an interaction
logger.log_interaction(
    prompt="What is machine learning?",
    response="Machine learning is a subset of artificial intelligence...",
    model="gpt-3.5-turbo",
    user_id="user123",
    tokens_used=150,
    latency_ms=250.5
)
```

### Using Context Manager for Automatic Timing

```python
from llm_logger import LLMTimer

with LLMTimer("Explain quantum computing", model="gpt-4") as timer:
    # Your LLM API call here
    response = call_llm_api(prompt)
    timer.set_response(response)
```

### Convenience Functions

```python
from llm_logger import log_llm_interaction, log_llm_error

# Quick logging
log_llm_interaction(
    prompt="Hello",
    response="Hi there!",
    model="gpt-3.5-turbo"
)

# Error logging
log_llm_error("API timeout", prompt="What is AI?")
```

## 🔧 Configuration

### Elasticsearch Configuration

- **Port**: 9200
- **Memory**: 512MB (adjustable in docker-compose.yml)
- **Index Pattern**: `llm-logs-YYYY.MM.dd`

### Logstash Configuration

- **Input**: File monitoring (`logs/llm_logs.json`)
- **Processing**: JSON parsing, field enrichment
- **Output**: Elasticsearch indexing

### Kibana Configuration

- **Port**: 5601
- **Default Data View**: `llm-logs-*`

## 📈 Analytics and Insights

### Key Metrics to Monitor

1. **Response Latency**: Track API performance
2. **Token Usage**: Monitor costs and efficiency
3. **Error Rates**: Identify reliability issues
4. **User Activity**: Understand usage patterns
5. **Model Performance**: Compare different models

### Sample Kibana Queries

```
# High latency requests
latency_ms:>1000

# Specific user activity
user_id:"user123"

# Error events
event_type:"error"

# Coding-related prompts
prompt_category:"coding"

# Token usage above threshold
tokens_used:>500
```

## 🔒 Security and Production Setup

### Enable Security (Production)

```bash
# Use the secure configuration
docker-compose -f security/docker-compose-secure.yml up -d
```

### Security Features

- HTTPS encryption
- Authentication with Elastic X-Pack
- Role-based access control
- TLS between services

### Best Practices

1. **Data Privacy**
   - Redact PII before logging
   - Implement data retention policies
   - Use encryption at rest

2. **Scalability**
   - Add Kafka for message queuing
   - Use multiple Elasticsearch nodes
   - Implement log rotation

3. **Monitoring**
   - Set up alerts for high error rates
   - Monitor disk usage
   - Track performance metrics

## 🔍 Troubleshooting

### Common Issues

#### Services Won't Start
```bash
# Check logs
docker-compose logs elasticsearch
docker-compose logs logstash
docker-compose logs kibana

# Restart services
docker-compose restart
```

#### No Data in Kibana
1. Check if logs are being generated: `ls -la logs/`
2. Verify Logstash is processing: `docker-compose logs logstash`
3. Check Elasticsearch indices: `curl localhost:9200/_cat/indices`

#### High Memory Usage
- Reduce Elasticsearch heap size in docker-compose.yml
- Limit Docker container memory

### Log File Permissions
```bash
# Ensure log directory is writable
chmod 755 logs/
```

## 🛠️ Development

### Running Tests

```bash
# Test logging functionality
python -c "from llm_logger import LLMLogger; LLMLogger().log_interaction('test', 'response')"

# Check log output
cat logs/llm_logs.json
```

### Custom Log Fields

Extend the logger to include custom fields:

```python
logger.log_interaction(
    prompt="Custom prompt",
    response="Custom response",
    custom_field="custom_value",
    experiment_id="exp_001"
)
```

## 📚 Resources

- [Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Logstash Documentation](https://www.elastic.co/guide/en/logstash/current/index.html)
- [Kibana Documentation](https://www.elastic.co/guide/en/kibana/current/index.html)
- [Docker Compose Reference](https://docs.docker.com/compose/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review Elasticsearch/Kibana logs
3. Create an issue with detailed information

---

**Happy Logging!** 🎉