#!/bin/bash

# Production deployment script for ELK Stack with security
# Run this script to set up a secure ELK stack for production use

set -e

echo "🔒 Setting up secure ELK Stack for LLM logging..."

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p security/certs
chmod 755 logs security/certs

# Check if we're running the secure version
if [ "$1" = "--secure" ]; then
    echo "🔐 Starting secure ELK stack..."
    
    # Start the setup service first to generate certificates
    echo "🔑 Generating SSL certificates..."
    docker-compose -f security/docker-compose-secure.yml up setup
    
    # Start the main services
    echo "🚀 Starting secure services..."
    docker-compose -f security/docker-compose-secure.yml up -d elasticsearch kibana logstash
    
    # Wait for services to be ready
    echo "⏳ Waiting for services to start..."
    sleep 30
    
    # Check service health
    echo "🏥 Checking service health..."
    
    # Wait for Elasticsearch
    until curl -s -k -u elastic:changeme https://localhost:9200/_cluster/health?wait_for_status=yellow&timeout=50s; do
        echo "Waiting for Elasticsearch..."
        sleep 10
    done
    
    echo "✅ Secure ELK stack is ready!"
    echo "🌐 Kibana: https://localhost:5601 (elastic/changeme)"
    echo "🔍 Elasticsearch: https://localhost:9200 (elastic/changeme)"
    
else
    echo "🚀 Starting basic ELK stack..."
    
    # Start basic stack
    docker-compose up -d
    
    # Wait for services
    echo "⏳ Waiting for services to start..."
    sleep 30
    
    # Check service health
    until curl -s http://localhost:9200/_cluster/health?wait_for_status=yellow&timeout=50s; do
        echo "Waiting for Elasticsearch..."
        sleep 10
    done
    
    echo "✅ Basic ELK stack is ready!"
    echo "🌐 Kibana: http://localhost:5601"
    echo "🔍 Elasticsearch: http://localhost:9200"
fi

echo ""
echo "📋 Next steps:"
echo "1. Generate sample data: python example_app.py"
echo "2. Open Kibana in your browser"
echo "3. Create data view: Stack Management → Kibana → Data Views"
echo "4. Use index pattern: llm-logs-* with timestamp field"
echo "5. Explore your data!"

echo ""
echo "🛠️ Useful commands:"
echo "  docker-compose ps                 # Check service status"
echo "  docker-compose logs [service]     # View service logs"
echo "  docker-compose down               # Stop all services"
echo "  docker-compose down -v            # Stop and remove volumes"

echo ""
echo "🔧 Configuration files:"
echo "  - Basic: docker-compose.yml"
echo "  - Secure: security/docker-compose-secure.yml"
echo "  - Logstash: logstash.conf"
echo "  - Logging: llm_logger.py"