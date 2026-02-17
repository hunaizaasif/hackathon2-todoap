#!/bin/bash
set -e

echo "🚀 Setting up Minikube with Ingress..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if minikube is installed
if ! command -v minikube &> /dev/null; then
    echo -e "${YELLOW}⚠️  Minikube is not installed. Please install it first.${NC}"
    echo "Visit: https://minikube.sigs.k8s.io/docs/start/"
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo -e "${YELLOW}⚠️  kubectl is not installed. Please install it first.${NC}"
    exit 1
fi

# Start Minikube if not running
echo -e "${BLUE}📦 Starting Minikube...${NC}"
minikube start --driver=docker --cpus=2 --memory=2048

# Enable ingress addon
echo -e "${BLUE}🔌 Enabling Ingress addon...${NC}"
minikube addons enable ingress

# Wait for ingress controller to be ready
echo -e "${BLUE}⏳ Waiting for ingress controller...${NC}"
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s

# Set docker environment to use minikube's docker daemon
echo -e "${BLUE}🐳 Configuring Docker environment...${NC}"
eval $(minikube docker-env)

# Build Docker images
echo -e "${BLUE}🏗️  Building Docker images...${NC}"

echo -e "${GREEN}Building backend image...${NC}"
cd phase-2
docker build -t phase2-backend:latest .
cd ..

echo -e "${GREEN}Building frontend image...${NC}"
cd phase-3/frontend
docker build -t phase3-frontend:latest .
cd ../..

echo -e "${GREEN}Building MCP server image...${NC}"
cd phase-3/mcp-server
docker build -t phase3-mcp-server:latest .
cd ../..

# Create secrets (if not exists)
echo -e "${BLUE}🔐 Creating secrets...${NC}"
if [ ! -f "k8s/secrets.yaml" ]; then
    echo -e "${YELLOW}⚠️  secrets.yaml not found. Please create it from secrets.yaml.example${NC}"
    echo "Run: cp k8s/secrets.yaml.example k8s/secrets.yaml"
    echo "Then edit k8s/secrets.yaml with your actual credentials"
    exit 1
fi

kubectl apply -f k8s/secrets.yaml

# Deploy applications
echo -e "${BLUE}🚀 Deploying applications...${NC}"
kubectl apply -f k8s/backend/
kubectl apply -f k8s/frontend/
kubectl apply -f k8s/mcp-server/
kubectl apply -f k8s/ingress/

# Wait for deployments
echo -e "${BLUE}⏳ Waiting for deployments to be ready...${NC}"
kubectl wait --for=condition=available --timeout=300s deployment/backend
kubectl wait --for=condition=available --timeout=300s deployment/frontend
kubectl wait --for=condition=available --timeout=300s deployment/mcp-server

# Get Minikube IP
MINIKUBE_IP=$(minikube ip)

# Add entry to /etc/hosts if not exists
echo -e "${BLUE}🌐 Configuring /etc/hosts...${NC}"
if ! grep -q "hackathon.local" /etc/hosts; then
    echo -e "${YELLOW}Adding hackathon.local to /etc/hosts (requires sudo)${NC}"
    echo "$MINIKUBE_IP hackathon.local" | sudo tee -a /etc/hosts
else
    echo -e "${GREEN}hackathon.local already in /etc/hosts${NC}"
fi

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo -e "${BLUE}📋 Access your application:${NC}"
echo "   Frontend: http://hackathon.local"
echo "   Backend API: http://hackathon.local/api"
echo "   MCP Server: http://hackathon.local/mcp"
echo ""
echo -e "${BLUE}🔍 Useful commands:${NC}"
echo "   kubectl get pods                    # Check pod status"
echo "   kubectl get services                # Check services"
echo "   kubectl get ingress                 # Check ingress"
echo "   kubectl logs -f deployment/backend  # View backend logs"
echo "   kubectl logs -f deployment/frontend # View frontend logs"
echo "   minikube dashboard                  # Open Kubernetes dashboard"
echo "   minikube tunnel                     # Create tunnel for LoadBalancer services"
echo ""
