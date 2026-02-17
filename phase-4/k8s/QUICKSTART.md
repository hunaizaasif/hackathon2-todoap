# Minikube Ingress - Quick Start Guide

Get your application running on Minikube in 5 minutes.

## Prerequisites

- Docker installed and running
- Minikube installed
- kubectl installed

## Step 1: Configure Secrets

```bash
# Copy the example file
cp k8s/secrets.yaml.example k8s/secrets.yaml

# Edit with your credentials
nano k8s/secrets.yaml
```

Update these values:
- `database-url`: Your Neon PostgreSQL connection string
- `auth-secret-key`: Generate with `openssl rand -hex 32`

## Step 2: Run Setup

```bash
# Make script executable
chmod +x k8s/setup-minikube.sh

# Run setup (takes 3-5 minutes)
./k8s/setup-minikube.sh
```

## Step 3: Access Application

Open in your browser:
- **Frontend**: http://hackathon.local
- **Backend API**: http://hackathon.local/api/docs
- **MCP Server**: http://hackathon.local/mcp

## Verify Deployment

```bash
# Check everything is working
chmod +x k8s/verify.sh
./k8s/verify.sh
```

## Common Commands

```bash
# View logs
kubectl logs -f deployment/backend
kubectl logs -f deployment/frontend

# Check status
kubectl get pods
kubectl get services
kubectl get ingress

# Restart a service
kubectl rollout restart deployment/backend

# Open dashboard
minikube dashboard
```

## Troubleshooting

### Can't access http://hackathon.local

1. Check Minikube IP: `minikube ip`
2. Verify /etc/hosts: `cat /etc/hosts | grep hackathon`
3. Add if missing: `echo "$(minikube ip) hackathon.local" | sudo tee -a /etc/hosts`

### Pods not starting

```bash
# Check pod status
kubectl get pods

# View logs
kubectl logs <pod-name>

# Describe pod
kubectl describe pod <pod-name>
```

### Images not found

Make sure you built images with Minikube's Docker:
```bash
eval $(minikube docker-env)
docker images  # Should show your images
```

## Cleanup

```bash
# Remove all resources
chmod +x k8s/cleanup.sh
./k8s/cleanup.sh

# Stop Minikube
minikube stop

# Delete cluster (optional)
minikube delete
```

## Need Help?

See the full documentation: [k8s/README.md](./README.md)
