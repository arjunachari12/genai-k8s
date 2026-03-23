# 05: Argo Rollouts Installation

## Objective

Install Argo Rollouts controller to enable progressive delivery capabilities like canary deployments.

## Prerequisites

- ArgoCD installed and running
- GenAI application deployed

## Step-by-step Instructions

### 1. Install Argo Rollouts

```bash
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
```

Wait for rollout controller to be ready:
```bash
kubectl wait --for=condition=Ready pod --all -n argo-rollouts --timeout=300s
```

### 2. Install Argo Rollouts CLI

```bash
# On Linux
curl -LO https://github.com/argoproj/argo-rollouts/releases/latest/download/kubectl-argo-rollouts-linux-amd64
chmod +x kubectl-argo-rollouts-linux-amd64
sudo mv kubectl-argo-rollouts-linux-amd64 /usr/local/bin/kubectl-argo-rollouts
```

### 3. Verify Installation

```bash
kubectl argo rollouts version
```

Check controller:
```bash
kubectl get pods -n argo-rollouts
```

### 4. Install Argo Rollouts Dashboard (Optional)

For UI visualization of rollouts:
```bash
kubectl apply -f https://github.com/argoproj/argo-rollouts/releases/latest/download/dashboard-install.yaml
```

Access dashboard:
```bash
kubectl port-forward svc/argo-rollouts-dashboard -n argo-rollouts 3100:3100
```

## Expected Output

- Argo Rollouts controller pod running
- CLI tool installed and functional
- Dashboard accessible at http://localhost:3100 (if installed)

## Validation Steps

1. Check controller status:
   ```bash
   kubectl get pods -n argo-rollouts
   ```

2. Verify CLI:
   ```bash
   kubectl argo rollouts version
   ```

3. List rollouts (should be empty for now):
   ```bash
   kubectl argo rollouts list rollouts -n genai-platform
   ```

## Troubleshooting

- **Controller not ready**: Check logs: `kubectl logs -n argo-rollouts deployment/argo-rollouts`
- **CLI install fails**: Ensure you have sudo permissions or adjust PATH
- **Dashboard not accessible**: Verify service exists and port-forward command

## What Just Happened?

You installed Argo Rollouts, which extends Kubernetes with progressive delivery capabilities. It allows you to perform canary deployments, blue-green deployments, and other rollout strategies.

## Challenge Exercise

Explore the Argo Rollouts dashboard (if installed) and note the different rollout strategies available. What CRDs were installed?