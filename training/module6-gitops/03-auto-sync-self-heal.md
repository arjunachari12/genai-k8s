# 03: Auto-Sync, Self-Healing, and Pruning

## Objective

Enable ArgoCD's auto-sync features to automatically deploy changes and maintain cluster state, including self-healing and pruning of resources.

## Prerequisites

- ArgoCD Application created (from Lab 02)
- Application currently in Manual sync mode

## Step-by-step Instructions

### 1. Enable Auto-Sync in ArgoCD UI

1. Open your `genai-platform` application in ArgoCD UI
2. Click "App Details" → "Edit"
3. Under "Sync Policy":
   - Check "Automatic"
   - Check "Prune Resources"
   - Check "Self Heal"
   - Set "Sync Options":
     - Allow Empty
     - Apply Out Of Sync Only
     - Prune Last
4. Save changes

### 2. Test Auto-Sync

Make a small change to trigger sync:
- Edit `helm/genai-platform/values.yaml` and change a replica count or image tag
- Commit the change (or just modify the file)

### 3. Observe Auto-Sync

Watch ArgoCD automatically detect and sync the change:
```bash
kubectl get applications -n argocd -w
```

### 4. Test Self-Healing

Manually delete a pod to trigger self-healing:
```bash
kubectl delete pod -l app=genai-api -n genai-platform
```

Watch ArgoCD recreate the pod.

### 5. Test Pruning

Add a resource to your Helm chart, then remove it. ArgoCD should prune the deleted resource.

## Expected Output

- Application syncs automatically when changes are detected
- Deleted pods are automatically recreated
- Removed resources are pruned from the cluster

## Validation Steps

1. Check application sync status:
   ```bash
   kubectl get applications genai-platform -n argocd -o yaml | grep syncPolicy
   ```

2. Verify self-healing:
   ```bash
   kubectl get pods -n genai-platform -w
   ```
   Delete a pod and watch it restart.

3. Check ArgoCD UI for sync history and health status.

## Troubleshooting

- **Auto-sync not triggering**: Ensure your repository is properly configured and accessible
- **Self-heal not working**: Check that the application has proper labels/selectors
- **Pruning fails**: Verify resource ownership and finalizers

## What Just Happened?

You enabled ArgoCD's GitOps automation features. Auto-sync keeps your cluster in sync with Git, self-healing maintains desired state, and pruning removes obsolete resources.

## Challenge Exercise

Create a ConfigMap in your Helm chart, deploy it, then remove it from the chart. Verify that ArgoCD prunes the ConfigMap automatically.