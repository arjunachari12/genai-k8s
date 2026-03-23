# 04: Drift Detection and Reconciliation

## Objective

Understand how ArgoCD detects configuration drift and reconciles the cluster back to the desired state defined in Git.

## Prerequisites

- ArgoCD Application with auto-sync enabled (from Lab 03)
- Application in healthy, synced state

## Step-by-step Instructions

### 1. Observe Current State

Check that your application is synced:
```bash
kubectl get applications genai-platform -n argocd
```
Should show "Synced" status.

### 2. Introduce Drift

Manually modify a deployed resource to create drift:

```bash
# Change a deployment's replica count
kubectl scale deployment genai-api --replicas=2 -n genai-platform
```

### 3. Observe Drift Detection

Watch ArgoCD detect the drift:
```bash
kubectl get applications genai-platform -n argocd -w
```

The status should change to "OutOfSync".

### 4. View Drift Details

In ArgoCD UI:
1. Open your application
2. Click "App Diff" to see the differences
3. Note the changes between desired (Git) and live (cluster) state

### 5. Trigger Reconciliation

ArgoCD should automatically reconcile (due to auto-sync). If not:
```bash
kubectl patch application genai-platform -n argocd --type merge -p '{"operation":{"sync":{}}}'
```

### 6. Verify Reconciliation

Check that the replica count returns to the original value:
```bash
kubectl get deployment genai-api -n genai-platform
```

## Expected Output

- ArgoCD detects the manual change as drift
- Application status shows "OutOfSync" temporarily
- Auto-sync reconciles the cluster back to Git state
- Replica count returns to original value

## Validation Steps

1. Check application status:
   ```bash
   kubectl get applications genai-platform -n argocd
   ```

2. Verify resource matches Git:
   ```bash
   kubectl get deployment genai-api -n genai-platform -o yaml | grep replicas
   ```

3. Check ArgoCD UI for sync history.

## Troubleshooting

- **Drift not detected**: Ensure ArgoCD has proper permissions and the resource is managed by the application
- **Reconciliation fails**: Check for validation webhooks or resource conflicts
- **Manual sync needed**: Verify auto-sync configuration

## What Just Happened?

ArgoCD continuously monitors your cluster for drift from the desired Git state. When drift is detected, it automatically reconciles by applying the Git-defined configuration.

## Challenge Exercise

Modify a ConfigMap value directly in the cluster and observe how ArgoCD detects and corrects the drift. What happens if you modify a Secret?