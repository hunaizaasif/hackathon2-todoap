#!/bin/bash
# Phase 4: Deploy Application using Helm
set -e

echo "🚀 Deploying Todo Application with Helm"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Create secrets if not exists
echo -e "${BLUE}🔐 Creating secrets...${NC}"
kubectl apply -f k8s/secrets.yaml

# Deploy backend
echo -e "${BLUE}📦 Deploying backend...${NC}"
helm upgrade --install backend ./helm/backend \
  --wait \
  --timeout 5m

# Deploy frontend
echo -e "${BLUE}📦 Deploying frontend...${NC}"
helm upgrade --install frontend ./helm/frontend \
  --wait \
  --timeout 5m

# Deploy ingress
echo -e "${BLUE}🌐 Deploying ingress...${NC}"
kubectl apply -f k8s/ingress/

# Wait for deployments
echo -e "${BLUE}⏳ Waiting for deployments...${NC}"
kubectl wait --for=condition=available --timeout=300s deployment/backend
kubectl wait --for=condition=available --timeout=300s deployment/frontend

# Get status
echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo -e "${BLUE}📊 Deployment Status:${NC}"
kubectl get deployments
echo ""
echo -e "${BLUE}📋 Pods:${NC}"
kubectl get pods
echo ""
echo -e "${BLUE}🌐 Services:${NC}"
kubectl get services
echo ""
echo -e "${BLUE}🔗 Ingress:${NC}"
kubectl get ingress
echo ""

MINIKUBE_IP=$(minikube ip)
echo -e "${BLUE}🎯 Access Application:${NC}"
echo "  1. Add to /etc/hosts:"
echo "     sudo sh -c 'echo \"$MINIKUBE_IP hackathon.local\" >> /etc/hosts'"
echo ""
echo "  2. Access at: http://hackathon.local"
echo ""
echo "  Or use port-forward:"
echo "     kubectl port-forward service/frontend 3000:3000"
echo "     kubectl port-forward service/backend 8080:7860"
echo ""
