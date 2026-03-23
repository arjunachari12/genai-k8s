# 08: Rollback Scenarios and Failure Handling

## Objective

Learn how to handle deployment failures with automated and manual rollback mechanisms in Argo Rollouts.

## Prerequisites

- Rollout with analysis configured (from Lab 07)
- Application running stable version
- ArgoCD CLI installed and logged in

## Step-by-step Instructions

### 1. Simulate Failure Scenario

Deploy a "bad" version that will fail analysis:
```yaml
# In genai-platform/helm/genai-platform/values.yaml
api:
  image:
    tag: "v2-bad"
```

Commit and push:
```bash
git add .
git commit -m "Deploy bad version v2-bad for rollback testing"
git push origin main
```

### 3. Observe Failure Detection

Watch the rollout status:
```bash
kubectl argo rollouts get rollout genai-api -n genai-platform -w
```

The rollout should show "Paused" or "Degraded" status.

### 4. Check Analysis Results

Examine the failed analysis:
```bash
kubectl describe analysisrun -n genai-platform
```

### 5. Automatic Rollback

If configured, the rollout should automatically rollback. Check:
```bash
kubectl argo rollouts get rollout genai-api -n genai-platform
```

### 6. Manual Rollback (if needed)

If auto-rollback didn't trigger:
```bash
kubectl argo rollouts abort genai-api -n genai-platform
kubectl argo rollouts undo genai-api -n genai-platform
```

### 7. Verify Rollback

Ensure traffic is back to stable version:
```bash
kubectl get pods -n genai-platform
```

All pods should be running the stable version.

### 8. Fix and Redeploy

Update to a good version:
```yaml
# In genai-platform/helm/genai-platform/values.yaml
api:
  image:
    tag: "v3-good"
```

Commit and push:
```bash
git add .
git commit -m "Deploy good version v3-good"
git push origin main
```

## Expected Output

- Rollout detects failure via analysis
- Traffic automatically rolls back to stable version
- New deployment succeeds with good metrics

## Validation Steps

1. Check rollout status:
   ```bash
   kubectl argo rollouts get rollout genai-api -n genai-platform
   ```

2. Verify pod versions:
   ```bash
   kubectl get pods -n genai-platform -o jsonpath='{.items[*].spec.containers[*].image}'
   ```

3. Check analysis run results:
   ```bash
   kubectl get analysisruns -n genai-platform
   ```

## Troubleshooting

- **Rollback not triggering**: Check analysis failure criteria and rollout configuration
- **Manual abort fails**: Ensure rollout is in correct state for abort
- **Traffic not switching**: Verify service selector and rollout labels

## What Just Happened?

You experienced automated failure detection and rollback. Argo Rollouts paused the canary when metrics indicated problems and rolled back to the stable version, preventing impact on users.

## Challenge Exercise

Configure the rollout to automatically abort on analysis failure without manual intervention. Test with a version that fails metrics and observe the automatic rollback.