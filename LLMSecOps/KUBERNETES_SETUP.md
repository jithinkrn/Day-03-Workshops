# Kubernetes Local Deployment Guide

## 🚀 Minikube Setup & Kubernetes Deployment

### Prerequisites
- Docker Desktop (already installed ✅)
- kubectl CLI
- minikube

## 📦 Installation Steps

### 1. Install minikube (macOS)
```bash
# Using Homebrew (recommended)
brew install minikube

# Alternative: Direct download
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-arm64
sudo install minikube-darwin-arm64 /usr/local/bin/minikube
```

### 2. Install kubectl (if not already installed)
```bash
# Using Homebrew
brew install kubectl

# Verify installation
kubectl version --client
```

### 3. Start minikube cluster
```bash
# Start minikube with Docker driver
minikube start --driver=docker

# Verify cluster status
minikube status
kubectl cluster-info
```

## 🔧 Kubernetes Configuration

### deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gpt-huggingface
  labels:
    app: gpt-huggingface
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gpt-hf-pod
  template:
    metadata:
      labels:
        app: gpt-hf-pod
    spec:
      containers:
      - name: gptcontainer
        image: 635671960272.dkr.ecr.ap-southeast-2.amazonaws.com/fastapi-app:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: gpt-hf-service
  labels:
    app: gpt-huggingface
spec:
  type: NodePort
  selector:
    app: gpt-hf-pod
  ports:
  - port: 8000
    targetPort: 8000
    nodePort: 30007
    protocol: TCP
    name: http
```

## 🚀 Deployment Commands

### Step 1: Configure ECR Access in minikube
```bash
# Configure AWS credentials for minikube
minikube ssh -- docker login --username AWS --password $(aws ecr get-login-password --region ap-southeast-2) 635671960272.dkr.ecr.ap-southeast-2.amazonaws.com
```

### Step 2: Deploy to Kubernetes
```bash
# Apply deployment
kubectl apply -f deployment.yaml

# Apply service
kubectl apply -f service.yaml

# Verify deployments
kubectl get deployments
kubectl get services
kubectl get pods
```

### Step 3: Check Status
```bash
# Watch pod creation
kubectl get pods -w

# Check deployment status
kubectl rollout status deployment/gpt-huggingface

# View deployment details
kubectl describe deployment gpt-huggingface
```

## 🔍 Verification Commands

### Pod and Service Status
```bash
# Get all resources
kubectl get all

# Check pod logs
kubectl logs -l app=gpt-hf-pod

# Describe service
kubectl describe service gpt-hf-service
```

### Port Forwarding (Alternative Access)
```bash
# Forward local port to service
kubectl port-forward service/gpt-hf-service 8080:8000

# Test via localhost
curl http://localhost:8080/health
```

### Minikube Service Access
```bash
# Get service URL
minikube service gpt-hf-service --url

# Open service in browser
minikube service gpt-hf-service
```

## 🧪 Testing the Deployment

### Health Check
```bash
# Get minikube IP and test
MINIKUBE_IP=$(minikube ip)
curl http://$MINIKUBE_IP:30007/health
```

### API Testing
```bash
# Test question-answering endpoint
curl -X POST http://$MINIKUBE_IP:30007/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What does Hugging Face provide?",
    "context": "Hugging Face is a technology company that provides open-source NLP libraries and tools for natural language processing."
  }'
```

## 📊 Monitoring & Scaling

### View Resource Usage
```bash
# Check resource usage
kubectl top nodes
kubectl top pods

# Monitor pods
watch kubectl get pods
```

### Scaling
```bash
# Scale deployment
kubectl scale deployment gpt-huggingface --replicas=5

# Check scaling
kubectl get deployment gpt-huggingface
```

### Rolling Updates
```bash
# Update image (example)
kubectl set image deployment/gpt-huggingface gptcontainer=635671960272.dkr.ecr.ap-southeast-2.amazonaws.com/fastapi-app:v2.0.0

# Check rollout status
kubectl rollout status deployment/gpt-huggingface

# Rollback if needed
kubectl rollout undo deployment/gpt-huggingface
```

## 🛠 Troubleshooting

### Common Issues

**Image Pull Errors:**
```bash
# Check if ECR authentication is working
kubectl describe pod <pod-name>

# Re-authenticate with ECR
minikube ssh -- docker login --username AWS --password $(aws ecr get-login-password --region ap-southeast-2) 635671960272.dkr.ecr.ap-southeast-2.amazonaws.com
```

**Pod CrashLoopBackOff:**
```bash
# Check pod logs
kubectl logs <pod-name>

# Describe pod for events
kubectl describe pod <pod-name>
```

**Service Not Accessible:**
```bash
# Check service endpoints
kubectl get endpoints gpt-hf-service

# Verify minikube tunnel
minikube tunnel
```

### Debug Commands
```bash
# Get into a pod
kubectl exec -it <pod-name> -- /bin/bash

# Check cluster events
kubectl get events --sort-by=.metadata.creationTimestamp

# Delete and recreate resources
kubectl delete -f deployment.yaml -f service.yaml
kubectl apply -f deployment.yaml -f service.yaml
```

## 🧹 Cleanup

### Remove Deployment
```bash
# Delete resources
kubectl delete -f deployment.yaml
kubectl delete -f service.yaml

# Or delete by name
kubectl delete deployment gpt-huggingface
kubectl delete service gpt-hf-service
```

### Stop minikube
```bash
# Stop minikube cluster
minikube stop

# Delete minikube cluster (complete cleanup)
minikube delete
```

## 🎯 Key Features of This Setup

### Deployment Features:
- ✅ **3 replicas** for high availability
- ✅ **Resource limits** to prevent resource exhaustion
- ✅ **Health probes** for automatic health checking
- ✅ **ECR integration** using your deployed image

### Service Features:
- ✅ **NodePort** for external access
- ✅ **Port 30007** for consistent access
- ✅ **Load balancing** across all pods

### Production Ready Features:
- 🔄 Rolling updates and rollbacks
- 📊 Resource monitoring and scaling
- 🔧 Health checks and self-healing
- 🌐 Service discovery and load balancing

## 📈 Next Steps

1. **Enable Ingress** for production-like routing
2. **Add ConfigMaps** for environment configuration
3. **Implement Secrets** for sensitive data
4. **Setup Persistent Volumes** if needed
5. **Add Horizontal Pod Autoscaler** for auto-scaling
6. **Configure Network Policies** for security