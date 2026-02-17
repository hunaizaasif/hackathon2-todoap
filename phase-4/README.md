# Phase 4: Cloud-Native & Orchestration

Transform the Todo application into a distributed, containerized system managed by Kubernetes.

## 📋 Overview

Phase 4 implements cloud-native orchestration using:
- **Kubernetes** for container orchestration
- **Minikube** for local cluster development
- **Helm** for package management
- **Docker** for containerization
- **Ingress** for routing

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Ingress Controller              │
│      (hackathon.local routing)          │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
┌───────▼────────┐  ┌──────▼────────┐
│   Frontend     │  │   Backend     │
│  (Next.js)     │  │  (FastAPI)    │
│  Port: 3000    │  │  Port: 7860   │
│  Replicas: 2   │  │  Replicas: 2  │
└────────────────┘  └───────┬───────┘
                            │
                    ┌───────▼────────┐
                    │  Neon PostgreSQL│
                    │  (External DB)  │
                    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker installed
- 4GB+ RAM available
- 2+ CPU cores

### Setup & Deploy

```bash
# 1. Setup Minikube cluster
cd phase-4
./scripts/setup.sh

# 2. Build Docker images
./scripts/build-images.sh

# 3. Deploy application
./scripts/deploy.sh
```

### Access Application

**Option 1: Via Ingress**
```bash
# Add to /etc/hosts
sudo sh -c 'echo "$(minikube ip) hackathon.local" >> /etc/hosts'

# Access at
http://hackathon.local
```

**Option 2: Via Port Forward**
```bash
kubectl port-forward service/frontend 3000:3000
kubectl port-forward service/backend 8080:7860

# Access at
http://localhost:3000
```

## 📁 Directory Structure

```
phase-4/
├── k8s/                    # Kubernetes manifests
│   ├── backend/           # Backend deployment & service
│   ├── frontend/          # Frontend deployment & service
│   ├── ingress/           # Ingress rules
│   └── secrets.yaml       # Secrets (database, API keys)
├── helm/                   # Helm charts
│   ├── backend/           # Backend Helm chart
│   │   ├── Chart.yaml
│   │   ├── values.yaml    # Default values
│   │   ├── values-dev.yaml
│   │   └── values-prod.yaml
│   └── frontend/          # Frontend Helm chart
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values-dev.yaml
│       └── values-prod.yaml
├── scripts/               # Automation scripts
│   ├── setup.sh          # Minikube setup
│   ├── build-images.sh   # Build Docker images
│   ├── deploy.sh         # Deploy with Helm
│   └── rollback.sh       # Rollback deployment
├── monitoring/            # AIOps & monitoring setup
│   └── README.md         # Monitoring guide
└── docs/                  # Documentation
    └── MONITORING.md     # Detailed monitoring setup
```

## 🔧 Common Operations

### Check Status
```bash
kubectl get pods              # Pod status
kubectl get deployments       # Deployment status
kubectl get services          # Service status
kubectl get ingress           # Ingress status
```

### View Logs
```bash
kubectl logs -f deployment/backend    # Backend logs
kubectl logs -f deployment/frontend   # Frontend logs
```

### Scale Deployments
```bash
# Using kubectl
kubectl scale deployment backend --replicas=3

# Using Helm
helm upgrade backend ./helm/backend --set replicaCount=3
```

### Rolling Updates
```bash
# Update backend
helm upgrade backend ./helm/backend --set image.tag=v2.0

# Update frontend
helm upgrade frontend ./helm/frontend --set image.tag=v2.0
```

### Rollback
```bash
# Rollback all
./scripts/rollback.sh

# Rollback specific component
./scripts/rollback.sh backend
./scripts/rollback.sh frontend
```

## 🎯 Deployment Strategies

### Zero-Downtime Updates

The application uses **rolling update** strategy:
- New pods are created before old ones are terminated
- Health checks ensure new pods are ready
- Automatic rollback on failure

Configuration in `values.yaml`:
```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
```

### Environment-Specific Deployments

```bash
# Development
helm upgrade backend ./helm/backend -f ./helm/backend/values-dev.yaml

# Production
helm upgrade backend ./helm/backend -f ./helm/backend/values-prod.yaml
```

## 📊 Monitoring

See [docs/MONITORING.md](docs/MONITORING.md) for detailed monitoring setup with AIOps tools.

Quick monitoring commands:
```bash
# Resource usage
kubectl top pods
kubectl top nodes

# Events
kubectl get events --sort-by='.lastTimestamp'

# Dashboard
minikube dashboard
```

## 🔐 Security

### Secrets Management

Secrets are stored in `k8s/secrets.yaml`:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: backend-secrets
type: Opaque
stringData:
  database-url: "postgresql://..."
  auth-secret-key: "..."
```

**⚠️ Important:** Never commit secrets to git. Use `.gitignore` or external secret management.

### Resource Limits

All pods have resource limits defined:
```yaml
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi
```

## 🐛 Troubleshooting

### Pods Not Starting
```bash
# Check pod status
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>

# Check events
kubectl get events
```

### Image Pull Errors
```bash
# Ensure Docker is using Minikube's daemon
eval $(minikube docker-env)

# Rebuild images
./scripts/build-images.sh
```

### Database Connection Issues
```bash
# Check secrets
kubectl get secret backend-secrets -o yaml

# Test connection from pod
kubectl exec -it deployment/backend -- env | grep DATABASE
```

### Ingress Not Working
```bash
# Check ingress controller
kubectl get pods -n ingress-nginx

# Check ingress rules
kubectl describe ingress app-ingress

# Use port-forward as alternative
kubectl port-forward service/frontend 3000:3000
```

## 📚 Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Phase 4 Spec](../../specs/001-cloud-native-orchestration/spec.md)

## ✅ Success Criteria

- [x] Applications deploy to local cluster within 5 minutes
- [x] Rolling updates complete without downtime
- [x] Failed deployments halt automatically
- [x] Deployment rollbacks work within 2 minutes
- [x] Pods pass health checks within 30 seconds
- [ ] AIOps monitoring integrated (see MONITORING.md)
- [ ] Helm charts support environment-specific configs

## 🤝 Contributing

When making changes:
1. Test locally with Minikube first
2. Update Helm chart values if needed
3. Document any new environment variables
4. Test rollback functionality
5. Update this README

---

**Status:** ✅ Deployed and Running
**Last Updated:** 2026-02-17
