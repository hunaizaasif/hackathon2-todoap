#!/bin/bash
set -e

echo "🧹 Cleaning up Kubernetes resources..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Delete all resources
echo -e "${BLUE}Deleting ingress...${NC}"
kubectl delete -f k8s/ingress/ --ignore-not-found=true

echo -e "${BLUE}Deleting backend...${NC}"
kubectl delete -f k8s/backend/ --ignore-not-found=true

echo -e "${BLUE}Deleting frontend...${NC}"
kubectl delete -f k8s/frontend/ --ignore-not-found=true

echo -e "${BLUE}Deleting MCP server...${NC}"
kubectl delete -f k8s/mcp-server/ --ignore-not-found=true

echo -e "${BLUE}Deleting secrets...${NC}"
kubectl delete secret backend-secrets --ignore-not-found=true

echo ""
echo -e "${GREEN}✅ Cleanup complete!${NC}"
echo ""
echo -e "${BLUE}To stop Minikube:${NC}"
echo "   minikube stop"
echo ""
echo -e "${BLUE}To delete Minikube cluster:${NC}"
echo "   minikube delete"
echo ""
