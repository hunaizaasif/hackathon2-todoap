#!/bin/bash
# Phase 4: Build Docker Images Script
set -e

echo "🏗️  Building Docker Images for Minikube"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configure Docker to use Minikube's daemon
echo -e "${BLUE}🐳 Configuring Docker environment...${NC}"
eval $(minikube docker-env)

# Build backend image
echo -e "${BLUE}📦 Building backend image...${NC}"
cd ../../phase-2
docker build -t phase2-backend:latest .
echo -e "${GREEN}✓ Backend image built${NC}"

# Build frontend image
echo -e "${BLUE}📦 Building frontend image...${NC}"
cd ../phase-3/frontend
docker build -t phase3-frontend:latest .
echo -e "${GREEN}✓ Frontend image built${NC}"

cd ../../phase-4

echo ""
echo -e "${GREEN}✅ All images built successfully!${NC}"
echo ""
echo -e "${BLUE}📋 Built images:${NC}"
docker images | grep -E "phase2-backend|phase3-frontend"
echo ""
echo -e "${BLUE}Next step:${NC} Deploy with ./scripts/deploy.sh"
echo ""
