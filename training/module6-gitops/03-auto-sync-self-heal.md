# 03: Auto-Sync, Self-Healing, and Pruning

## Objective

Enable ArgoCD's auto-sync features to automatically deploy changes and maintain cluster state, including self-healing and pruning of resources.

## Prerequisites

- ArgoCD Application created and synced (from Lab 02)
- Application currently in Manual sync mode
- ArgoCD CLI installed and logged in

## Step-by-step Instructions

### 1. Enable Auto-Sync via CLI

```bash
# Enable auto-sync, self-heal, and prune
argocd app set genai-platform \
  --sync-policy automated \
  --self-heal \
  --prune
```

### 2. Test Auto-Sync

Make a small change to trigger sync:
```bash
# Edit values.yaml to change replica count
sed -i 's/replicaCount: [0-9]/replicaCount: 2/' genai-platform/helm/genai-platform/values.yaml
git add .
git commit -m "Update replica count to 2"
git push origin main
```

### 3. Observe Auto-Sync

Watch ArgoCD automatically detect and sync the change:
```bash
argocd app get genai-platform --watch
```

### 4. Test Self-Healing

Manually delete a pod to trigger self-healing:
```bash
kubectl delete pod -l app.kubernetes.io/name=genai-platform -n genai-platform --wait=false
```

Watch ArgoCD recreate the pod automatically.

### 5. Test Pruning

Add a resource to your Helm chart, deploy it, then remove it. ArgoCD should prune the deleted resource.

## Expected Output

- Application syncs automatically when changes are detected
- Deleted pods are automatically recreated
- Removed resources are pruned from the cluster

## Validation Steps

1. Check application sync status:
   ```bash
   argocd app get genai-platform
   ```

2. Verify self-healing:
   ```bash
   kubectl get pods -n genai-platform -w
   ```
   Delete a pod and watch it restart.

3. Check ArgoCD sync history:
   ```bash
   argocd app history genai-platform
   ```

## Troubleshooting

- **Auto-sync not triggering**: Ensure your repository is properly configured and accessible
- **Self-heal not working**: Check that the application has proper labels/selectors
- **Pruning fails**: Verify resource ownership and finalizers

## What Just Happened?

You enabled ArgoCD's GitOps automation features. Auto-sync keeps your cluster in sync with Git, self-healing maintains desired state, and pruning removes obsolete resources.

## Challenge Exercise

Create a ConfigMap in your Helm chart, deploy it, then remove it from the chart. Verify that ArgoCD prunes the ConfigMap automatically.