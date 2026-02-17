# Monitoring & AIOps Setup Guide

This guide covers setting up monitoring and AIOps tools for the Kubernetes cluster.

## 📊 Overview

Phase 4 supports monitoring through:
- **kubectl** built-in commands
- **Minikube Dashboard** for visualization
- **kubectl-ai** or **kagent** for AIOps (optional)

## 🚀 Quick Monitoring

### Built-in Kubernetes Monitoring

```bash
# Pod status
kubectl get pods -w

# Resource usage (requires metrics-server)
kubectl top pods
kubectl top nodes

# Events
kubectl get events --sort-by='.lastTimestamp'

# Logs
kubectl logs -f deployment/backend
kubectl logs -f deployment/frontend
```

### Minikube Dashboard

```bash
# Open dashboard
minikube dashboard

# Dashboard shows:
# - Pod status and logs
# - Resource usage
# - Deployments and services
# - Events and errors
```

## 🤖 AIOps Integration

### Option 1: kubectl-ai

kubectl-ai provides AI-powered cluster diagnostics.

**Installation:**
```bash
# Install kubectl-ai
curl -LO https://github.com/sozercan/kubectl-ai/releases/latest/download/kubectl-ai_linux_amd64.tar.gz
tar -xzf kubectl-ai_linux_amd64.tar.gz
mv kubectl-ai ~/.local/bin/
chmod +x ~/.local/bin/kubectl-ai

# Configure OpenAI API key
export OPENAI_API_KEY="your-api-key"
```

**Usage:**
```bash
# Diagnose issues
kubectl ai "why is my pod crashing?"
kubectl ai "how to fix ImagePullBackOff error?"
kubectl ai "optimize resource usage"
```

### Option 2: kagent

kagent provides intelligent cluster monitoring and recommendations.

**Installation:**
```bash
# Install kagent
kubectl apply -f https://raw.githubusercontent.com/kubeshop/kagent/main/deploy/kagent.yaml

# Wait for deployment
kubectl wait --for=condition=available --timeout=120s deployment/kagent -n kagent-system
```

**Usage:**
```bash
# Check cluster health
kubectl kagent health

# Get recommendations
kubectl kagent recommend

# Analyze issues
kubectl kagent analyze
```

## 📈 Metrics Server Setup

Enable metrics for resource monitoring:

```bash
# Enable metrics-server addon
minikube addons enable metrics-server

# Wait for metrics to be available
kubectl wait --for=condition=available --timeout=120s deployment/metrics-server -n kube-system

# Check resource usage
kubectl top pods
kubectl top nodes
```

## 🔔 Alert Configuration

### Basic Alerting with kubectl

Create a monitoring script:

```bash
#!/bin/bash
# monitor.sh - Basic cluster monitoring

while true; do
    # Check for unhealthy pods
    UNHEALTHY=$(kubectl get pods --field-selector=status.phase!=Running -o json | jq '.items | length')

    if [ "$UNHEALTHY" -gt 0 ]; then
        echo "⚠️  Alert: $UNHEALTHY unhealthy pods detected"
        kubectl get pods --field-selector=status.phase!=Running
    fi

    # Check resource usage
    CPU_USAGE=$(kubectl top nodes | awk 'NR==2 {print $3}' | sed 's/%//')
    if [ "$CPU_USAGE" -gt 80 ]; then
        echo "⚠️  Alert: High CPU usage: ${CPU_USAGE}%"
    fi

    sleep 60
done
```

## 📊 Monitoring Best Practices

### 1. Health Checks

Ensure all deployments have proper health checks:

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 7860
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /health
    port: 7860
  initialDelaySeconds: 10
  periodSeconds: 5
```

### 2. Resource Monitoring

Monitor resource usage regularly:

```bash
# Create monitoring alias
alias k8s-monitor='watch -n 5 "kubectl top pods && echo && kubectl get pods"'

# Use it
k8s-monitor
```

### 3. Log Aggregation

Collect logs from all pods:

```bash
# Stream all logs
kubectl logs -f -l app=backend --all-containers=true

# Save logs to file
kubectl logs deployment/backend > backend-logs.txt
kubectl logs deployment/frontend > frontend-logs.txt
```

### 4. Event Monitoring

Watch for important events:

```bash
# Watch events in real-time
kubectl get events -w

# Filter warning events
kubectl get events --field-selector type=Warning
```

## 🎯 Monitoring Checklist

- [ ] Metrics server enabled
- [ ] Health checks configured for all pods
- [ ] Resource limits set appropriately
- [ ] Logging strategy in place
- [ ] Alert mechanism configured
- [ ] Dashboard access verified
- [ ] AIOps tool installed (optional)

## 🐛 Common Monitoring Scenarios

### Scenario 1: Pod Keeps Restarting

```bash
# Check pod status
kubectl describe pod <pod-name>

# Check logs from previous container
kubectl logs <pod-name> --previous

# Check events
kubectl get events --field-selector involvedObject.name=<pod-name>
```

### Scenario 2: High Resource Usage

```bash
# Check resource usage
kubectl top pods

# Check resource limits
kubectl describe pod <pod-name> | grep -A 5 "Limits"

# Scale down if needed
kubectl scale deployment <name> --replicas=1
```

### Scenario 3: Service Not Responding

```bash
# Check service endpoints
kubectl get endpoints

# Test service from within cluster
kubectl run test --rm -it --image=busybox -- wget -O- http://backend:7860/health

# Check ingress
kubectl describe ingress app-ingress
```

## 📚 Additional Resources

- [Kubernetes Monitoring Guide](https://kubernetes.io/docs/tasks/debug/debug-cluster/)
- [kubectl-ai GitHub](https://github.com/sozercan/kubectl-ai)
- [kagent Documentation](https://github.com/kubeshop/kagent)
- [Minikube Metrics](https://minikube.sigs.k8s.io/docs/tutorials/metrics/)

## 🔄 Next Steps

1. Enable metrics-server: `minikube addons enable metrics-server`
2. Install AIOps tool of choice (kubectl-ai or kagent)
3. Set up monitoring dashboard
4. Configure alerts for critical events
5. Document monitoring procedures for your team

---

**Note:** For production deployments, consider using:
- Prometheus + Grafana for metrics
- ELK Stack for log aggregation
- PagerDuty/Opsgenie for alerting
