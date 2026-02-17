#!/bin/bash

echo "🔍 Verifying Minikube deployment..."

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if minikube is running
echo -e "${BLUE}Checking Minikube status...${NC}"
if minikube status | grep -q "Running"; then
    echo -e "${GREEN}✓ Minikube is running${NC}"
else
    echo -e "${RED}✗ Minikube is not running${NC}"
    exit 1
fi

# Check ingress addon
echo -e "${BLUE}Checking Ingress addon...${NC}"
if minikube addons list | grep ingress | grep -q enabled; then
    echo -e "${GREEN}✓ Ingress addon is enabled${NC}"
else
    echo -e "${RED}✗ Ingress addon is not enabled${NC}"
fi

# Check pods
echo -e "${BLUE}Checking pods...${NC}"
BACKEND_POD=$(kubectl get pods -l app=backend -o jsonpath='{.items[0].status.phase}' 2>/dev/null)
FRONTEND_POD=$(kubectl get pods -l app=frontend -o jsonpath='{.items[0].status.phase}' 2>/dev/null)
MCP_POD=$(kubectl get pods -l app=mcp-server -o jsonpath='{.items[0].status.phase}' 2>/dev/null)

if [ "$BACKEND_POD" = "Running" ]; then
    echo -e "${GREEN}✓ Backend pod is running${NC}"
else
    echo -e "${RED}✗ Backend pod status: $BACKEND_POD${NC}"
fi

if [ "$FRONTEND_POD" = "Running" ]; then
    echo -e "${GREEN}✓ Frontend pod is running${NC}"
else
    echo -e "${RED}✗ Frontend pod status: $FRONTEND_POD${NC}"
fi

if [ "$MCP_POD" = "Running" ]; then
    echo -e "${GREEN}✓ MCP server pod is running${NC}"
else
    echo -e "${RED}✗ MCP server pod status: $MCP_POD${NC}"
fi

# Check services
echo -e "${BLUE}Checking services...${NC}"
kubectl get services | grep -E "backend|frontend|mcp-server" | while read line; do
    echo -e "${GREEN}✓ $line${NC}"
done

# Check ingress
echo -e "${BLUE}Checking ingress...${NC}"
INGRESS_STATUS=$(kubectl get ingress app-ingress -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null)
if [ -n "$INGRESS_STATUS" ]; then
    echo -e "${GREEN}✓ Ingress is configured${NC}"
else
    echo -e "${YELLOW}⚠ Ingress IP not yet assigned (this is normal, may take a minute)${NC}"
fi

# Check /etc/hosts
echo -e "${BLUE}Checking /etc/hosts...${NC}"
if grep -q "hackathon.local" /etc/hosts; then
    echo -e "${GREEN}✓ hackathon.local is in /etc/hosts${NC}"
else
    echo -e "${RED}✗ hackathon.local not found in /etc/hosts${NC}"
    MINIKUBE_IP=$(minikube ip)
    echo -e "${YELLOW}Run: echo '$MINIKUBE_IP hackathon.local' | sudo tee -a /etc/hosts${NC}"
fi

# Test endpoints
echo -e "${BLUE}Testing endpoints...${NC}"

# Test frontend
if curl -s -o /dev/null -w "%{http_code}" http://hackathon.local | grep -q "200\|301\|302"; then
    echo -e "${GREEN}✓ Frontend is accessible at http://hackathon.local${NC}"
else
    echo -e "${RED}✗ Frontend is not accessible${NC}"
fi

# Test backend
if curl -s -o /dev/null -w "%{http_code}" http://hackathon.local/api/health | grep -q "200"; then
    echo -e "${GREEN}✓ Backend API is accessible at http://hackathon.local/api${NC}"
else
    echo -e "${YELLOW}⚠ Backend API health check failed (may need time to start)${NC}"
fi

echo ""
echo -e "${BLUE}📋 Quick commands:${NC}"
echo "   kubectl get pods              # View all pods"
echo "   kubectl logs -f deployment/backend   # Backend logs"
echo "   kubectl logs -f deployment/frontend  # Frontend logs"
echo "   minikube dashboard            # Open dashboard"
echo ""
