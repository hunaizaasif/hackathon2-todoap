#!/bin/bash
# Phase 4: Minikube Setup Script
set -e

echo "🚀 Phase 4: Cloud-Native Orchestration Setup"
echo "=============================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check prerequisites
echo -e "${BLUE}📋 Checking prerequisites...${NC}"

if ! command -v minikube &> /dev/null; then
    echo -e "${YELLOW}⚠️  Minikube not found. Installing...${NC}"
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    install minikube-linux-amd64 ~/.local/bin/minikube
    rm minikube-linux-amd64
fi

if ! command -v kubectl &> /dev/null; then
    echo -e "${YELLOW}⚠️  kubectl not found. Please install kubectl first.${NC}"
    exit 1
fi

if ! command -v helm &> /dev/null; then
    echo -e "${YELLOW}⚠️  Helm not found. Installing...${NC}"
    cd /tmp
    wget https://get.helm.sh/helm-v3.20.0-linux-amd64.tar.gz
    tar -zxvf helm-v3.20.0-linux-amd64.tar.gz
    mv linux-amd64/helm ~/.local/bin/
    rm -rf linux-amd64 helm-v3.20.0-linux-amd64.tar.gz
fi

echo -e "${GREEN}✓ Prerequisites checked${NC}"
echo ""

# Start Minikube
echo -e "${BLUE}🎯 Starting Minikube cluster...${NC}"
minikube start --driver=docker --cpus=2 --memory=2048 --force || {
    echo -e "${YELLOW}Minikube already running or failed to start${NC}"
}

# Enable ingress
echo -e "${BLUE}🔌 Enabling Ingress addon...${NC}"
minikube addons enable ingress

# Wait for ingress controller
echo -e "${BLUE}⏳ Waiting for ingress controller...${NC}"
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s

# Configure Docker environment
echo -e "${BLUE}🐳 Configuring Docker environment...${NC}"
eval $(minikube docker-env)

echo ""
echo -e "${GREEN}✅ Minikube setup complete!${NC}"
echo ""
echo -e "${BLUE}📋 Next steps:${NC}"
echo "  1. Build Docker images: cd ../.. && ./phase-4/scripts/build-images.sh"
echo "  2. Deploy application: ./phase-4/scripts/deploy.sh"
echo ""
echo -e "${BLUE}🔍 Useful commands:${NC}"
echo "  minikube status          # Check cluster status"
echo "  minikube dashboard       # Open Kubernetes dashboard"
echo "  kubectl get pods         # Check pod status"
echo ""
