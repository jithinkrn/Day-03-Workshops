# ECR Deployment Guide

## Prerequisites
- AWS CLI installed and configured ✅
- Docker image built locally (`fastapi-app`) ✅
- AWS account with ECR permissions

## Step-by-Step ECR Deployment

### Step 1: Create ECR Repository (if it doesn't exist)
```bash
# Replace 'your-region' with your AWS region (e.g., us-east-1, eu-west-1)
aws ecr create-repository --repository-name fastapi-app --region your-region
```

### Step 2: Get ECR Login Token
```bash
# Get login token and authenticate Docker to ECR
aws ecr get-login-password --region your-region | docker login --username AWS --password-stdin your-account-id.dkr.ecr.your-region.amazonaws.com
```

### Step 3: Tag Your Docker Image
```bash
# Tag your local image for ECR
docker tag fastapi-app:latest your-account-id.dkr.ecr.your-region.amazonaws.com/fastapi-app:latest

# Optional: Tag with version
docker tag fastapi-app:latest your-account-id.dkr.ecr.your-region.amazonaws.com/fastapi-app:v1.0.0
```

### Step 4: Push to ECR
```bash
# Push the tagged image
docker push your-account-id.dkr.ecr.your-region.amazonaws.com/fastapi-app:latest

# Optional: Push version tag
docker push your-account-id.dkr.ecr.your-region.amazonaws.com/fastapi-app:v1.0.0
```

## Example with Real Values

Replace these placeholder values:
- `your-account-id`: Your AWS Account ID (12 digits)
- `your-region`: Your AWS region (e.g., `us-east-1`)
- `fastapi-app`: Your ECR repository name

### Example Commands:
```bash
# Example for us-east-1 region and account ID 123456789012
aws ecr create-repository --repository-name fastapi-app --region us-east-1

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

docker tag fastapi-app:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/fastapi-app:latest

docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/fastapi-app:latest
```

## Getting Your AWS Account Information

### Get Account ID:
```bash
aws sts get-caller-identity --query Account --output text
```

### Get Current Region:
```bash
aws configure get region
```

## Next Steps After Push

1. **Verify Push**: Check ECR console or use CLI:
   ```bash
   aws ecr describe-images --repository-name fastapi-app --region your-region
   ```

2. **Deploy to ECS/EKS**: Use the ECR image URI in your container definitions

3. **Security Scanning**: ECR can automatically scan images for vulnerabilities

4. **Image Lifecycle**: Set up lifecycle policies to manage old images

## Troubleshooting

### Common Issues:
1. **Permission Denied**: Ensure your AWS credentials have ECR permissions
2. **Repository Not Found**: Create the repository first
3. **Authentication Failed**: Re-run the ECR login command
4. **Region Mismatch**: Ensure consistent region usage

### Required IAM Permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "ecr:InitiateLayerUpload",
                "ecr:UploadLayerPart",
                "ecr:CompleteLayerUpload",
                "ecr:PutImage"
            ],
            "Resource": "*"
        }
    ]
}
```