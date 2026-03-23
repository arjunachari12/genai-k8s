# 04: Drift Detection and Reconciliation

## Objective

Understand how ArgoCD detects configuration drift and reconciles the cluster back to the desired state defined in Git.

## Prerequisites

- ArgoCD Application with auto-sync enabled (from Lab 03)
- Application in healthy, synced state
- ArgoCD CLI installed and logged in

## Step-by-step Instructions

### 1. Observe Current State

Check that your application is synced:
```bash
argocd app get genai-platform
```
Should show "Synced" status.

### 2. Introduce Drift

Manually modify a deployed resource to create drift:

```bash
# Change a deployment's replica count
kubectl scale deployment -l app.kubernetes.io/name=genai-platform --replicas=1 -n genai-platform
```

### 3. Observe Drift Detection

Watch ArgoCD detect the drift:
```bash
argocd app get genai-platform --watch
```

The status should change to "OutOfSync".

### 4. View Drift Details

```bash
# Get detailed diff
argocd app diff genai-platform
```

### 5. Trigger Reconciliation

ArgoCD should automatically reconcile (due to auto-sync). If not:
```bash
argocd app sync genai-platform
```

### 6. Verify Reconciliation

Check that the replica count returns to the original value:
```bash
kubectl get deployment -l app.kubernetes.io/name=genai-platform -n genai-platform
```

## Expected Output

- ArgoCD detects the manual change as drift
- Application status shows "OutOfSync" temporarily
- Auto-sync reconciles the cluster back to Git state
- Replica count returns to original value

## Validation Steps

1. Check application status:
   ```bash
   argocd app get genai-platform
   ```

2. Verify resource matches Git:
   ```bash
   kubectl get deployment -l app.kubernetes.io/name=genai-platform -n genai-platform -o jsonpath='{.spec.replicas}'
   ```

3. Check sync history:
   ```bash
   argocd app history genai-platform
   ```

## Troubleshooting

- **Drift not detected**: Ensure ArgoCD has proper permissions and the resource is managed by the application
- **Reconciliation fails**: Check for validation webhooks or resource conflicts
- **Manual sync needed**: Verify auto-sync configuration

## What Just Happened?

ArgoCD continuously monitors your cluster for drift from the desired Git state. When drift is detected, it automatically reconciles by applying the Git-defined configuration.

## Challenge Exercise

Modify a ConfigMap value directly in the cluster and observe how ArgoCD detects and corrects the drift. What happens if you modify a Secret?