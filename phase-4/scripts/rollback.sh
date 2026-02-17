#!/bin/bash
# Phase 4: Rollback Deployment Script
set -e

echo "⏪ Rolling Back Deployment"
echo "=========================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check which component to rollback
COMPONENT=${1:-all}

if [ "$COMPONENT" = "backend" ] || [ "$COMPONENT" = "all" ]; then
    echo -e "${BLUE}⏪ Rolling back backend...${NC}"
    helm rollback backend
    echo -e "${GREEN}✓ Backend rolled back${NC}"
fi

if [ "$COMPONENT" = "frontend" ] || [ "$COMPONENT" = "all" ]; then
    echo -e "${BLUE}⏪ Rolling back frontend...${NC}"
    helm rollback frontend
    echo -e "${GREEN}✓ Frontend rolled back${NC}"
fi

# Wait for rollback to complete
echo -e "${BLUE}⏳ Waiting for rollback to complete...${NC}"
kubectl wait --for=condition=available --timeout=120s deployment/backend 2>/dev/null || true
kubectl wait --for=condition=available --timeout=120s deployment/frontend 2>/dev/null || true

echo ""
echo -e "${GREEN}✅ Rollback complete!${NC}"
echo ""
echo -e "${BLUE}📊 Current Status:${NC}"
kubectl get pods
echo ""
echo -e "${BLUE}Usage:${NC}"
echo "  ./rollback.sh           # Rollback all components"
echo "  ./rollback.sh backend   # Rollback backend only"
echo "  ./rollback.sh frontend  # Rollback frontend only"
echo ""
