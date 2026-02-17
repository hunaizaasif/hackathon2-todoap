# Kubernetes Deployment with Minikube

This directory contains Kubernetes manifests for deploying the application stack on Minikube with Ingress.

## Architecture

```
                    ┌─────────────────┐
                    │  Ingress (Nginx)│
                    │ hackathon.local │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │   Frontend   │ │   Backend    │ │  MCP Server  │
    │   (Next.js)  │ │  (FastAPI)   │ │   (Node.js)  │
    │   Port 3000  │ │  Port 7860   │ │  Port 7860   │
    └──────────────┘ └──────────────┘ └──────────────┘
```

## Routes

- `http://hackathon.local/` → Frontend (Next.js)
- `http://hackathon.local/api/*` → Backend API (FastAPI)
- `http://hackathon.local/mcp/*` → MCP Server (Node.js)

## Prerequisites

1. **Minikube** - Local Kubernetes cluster
   ```bash
   # Install on Linux
   curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
   sudo install minikube-linux-amd64 /usr/local/bin/minikube
   ```

2. **kubectl** - Kubernetes CLI
   ```bash
   # Install on Linux
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
   ```

3. **Docker** - Container runtime (required by Minikube)

## Quick Start

### 1. Configure Secrets

```bash
# Copy the example secrets file
cp k8s/secrets.yaml.example k8s/secrets.yaml

# Edit with your actual credentials
nano k8s/secrets.yaml
```

Update the following values:
- `database-url`: Your Neon PostgreSQL connection string
- `auth-secret-key`: Generate with `openssl rand -hex 32`

### 2. Run Setup Script

```bash
# Make script executable (if not already)
chmod +x k8s/setup-minikube.sh

# Run the setup
./k8s/setup-minikube.sh
```

The script will:
- Start Minikube
- Enable Ingress addon
- Build Docker images
- Deploy all services
- Configure /etc/hosts

### 3. Access the Application

Open your browser and navigate to:
- **Frontend**: http://hackathon.local
- **Backend API**: http://hackathon.local/api/docs (Swagger UI)
- **MCP Server**: http://hackathon.local/mcp

## Manual Deployment

If you prefer manual steps:

### 1. Start Minikube

```bash
minikube start --driver=docker --cpus=4 --memory=4096
minikube addons enable ingress
```

### 2. Build Images

```bash
# Use Minikube's Docker daemon
eval $(minikube docker-env)

# Build backend
cd phase-2
docker build -t phase2-backend:latest .

# Build frontend
cd ../phase-3/frontend
docker build -t phase3-frontend:latest .

# Build MCP server
cd ../mcp-server
docker build -t phase3-mcp-server:latest .
cd ../../..
```

### 3. Deploy to Kubernetes

```bash
# Create secrets
kubectl apply -f k8s/secrets.yaml

# Deploy services
kubectl apply -f k8s/backend/
kubectl apply -f k8s/frontend/
kubectl apply -f k8s/mcp-server/
kubectl apply -f k8s/ingress/
```

### 4. Configure /etc/hosts

```bash
# Get Minikube IP
MINIKUBE_IP=$(minikube ip)

# Add to /etc/hosts
echo "$MINIKUBE_IP hackathon.local" | sudo tee -a /etc/hosts
```

## Useful Commands

### Check Status

```bash
# View all pods
kubectl get pods

# View services
kubectl get services

# View ingress
kubectl get ingress

# Describe ingress (detailed info)
kubectl describe ingress app-ingress
```

### View Logs

```bash
# Backend logs
kubectl logs -f deployment/backend

# Frontend logs
kubectl logs -f deployment/frontend

# MCP server logs
kubectl logs -f deployment/mcp-server

# Ingress controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx
```

### Debug

```bash
# Get pod details
kubectl describe pod <pod-name>

# Execute command in pod
kubectl exec -it <pod-name> -- /bin/sh

# Port forward (bypass ingress)
kubectl port-forward deployment/backend 7860:7860
kubectl port-forward deployment/frontend 3000:3000
```

### Restart Deployments

```bash
kubectl rollout restart deployment/backend
kubectl rollout restart deployment/frontend
kubectl rollout restart deployment/mcp-server
```

### Scale Deployments

```bash
# Scale to 3 replicas
kubectl scale deployment/backend --replicas=3

# Scale to 1 replica
kubectl scale deployment/backend --replicas=1
```

## Minikube Dashboard

```bash
# Open Kubernetes dashboard
minikube dashboard
```

## Cleanup

```bash
# Delete all resources
kubectl delete -f k8s/ingress/
kubectl delete -f k8s/backend/
kubectl delete -f k8s/frontend/
kubectl delete -f k8s/mcp-server/
kubectl delete -f k8s/secrets.yaml

# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete
```

## Troubleshooting

### Ingress not working

```bash
# Check ingress controller status
kubectl get pods -n ingress-nginx

# Check ingress configuration
kubectl describe ingress app-ingress

# Test ingress controller
curl -H "Host: hackathon.local" http://$(minikube ip)
```

### Pods not starting

```bash
# Check pod status
kubectl get pods

# View pod logs
kubectl logs <pod-name>

# Describe pod for events
kubectl describe pod <pod-name>
```

### Image pull errors

Make sure you're using Minikube's Docker daemon:
```bash
eval $(minikube docker-env)
docker images  # Should show your built images
```

### Database connection issues

```bash
# Check secrets
kubectl get secret backend-secrets -o yaml

# Verify DATABASE_URL in pod
kubectl exec -it <backend-pod-name> -- env | grep DATABASE_URL
```

## Production Considerations

For production deployment:

1. **Use proper image registry** (Docker Hub, ECR, GCR)
2. **Configure resource limits** appropriately
3. **Set up horizontal pod autoscaling** (HPA)
4. **Use proper secrets management** (Sealed Secrets, External Secrets)
5. **Configure persistent volumes** for stateful data
6. **Set up monitoring** (Prometheus, Grafana)
7. **Configure TLS/SSL** certificates
8. **Use proper domain names** instead of .local
9. **Implement health checks** and readiness probes
10. **Set up CI/CD pipelines** for automated deployments

## Next Steps

- [ ] Configure TLS certificates
- [ ] Set up monitoring and logging
- [ ] Implement horizontal pod autoscaling
- [ ] Add persistent volumes for data
- [ ] Configure backup and disaster recovery
- [ ] Set up CI/CD pipeline
