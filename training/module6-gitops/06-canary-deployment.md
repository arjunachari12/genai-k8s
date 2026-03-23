# 06: Implementing Canary Deployment

## Objective

Replace your standard Deployment with an Argo Rollouts Rollout CR to implement canary deployment strategy with gradual traffic shifting.

## Prerequisites

- Argo Rollouts installed (from Lab 05)
- ArgoCD Application managing your app

## Step-by-step Instructions

### 1. Examine Current Deployment

Check your current deployment:
```bash
kubectl get deployment -n genai-platform
```

### 2. Create Rollout Manifest

Apply the provided `rollout.yaml`:
```bash
kubectl apply -f training/manifests/rollout.yaml
```

This replaces your Deployment with a Rollout.

### 3. Update ArgoCD Application

Since we changed from Deployment to Rollout, update your ArgoCD app to ignore the old Deployment:
- In ArgoCD UI, edit your application
- Add to "Resource Exclusions": `apps/Deployment`

Or via CLI:
```bash
kubectl patch application genai-platform -n argocd --type merge -p '{"spec":{"ignoreDifferences":[{"group":"apps","kind":"Deployment","name":"genai-api"}]}}'
```

### 4. Deploy New Version

Update the image tag in your Helm values to trigger a canary rollout:
```yaml
# In helm/genai-platform/values.yaml
api:
  image:
    tag: "v2"  # Change from v1
```

Commit and let ArgoCD sync.

### 5. Monitor Canary Rollout

Watch the rollout progress:
```bash
kubectl argo rollouts get rollout genai-api -n genai-platform -w
```

### 6. Promote Rollout

Once analysis passes (we'll add this later), promote to full rollout:
```bash
kubectl argo rollouts promote genai-api -n genai-platform
```

## Expected Output

- Rollout CR created
- Canary deployment starts with 20% traffic to new version
- Gradual traffic increase: 20% → 50% → 100%
- Rollout completes successfully

## Validation Steps

1. Check rollout status:
   ```bash
   kubectl argo rollouts get rollout genai-api -n genai-platform
   ```

2. Verify pods:
   ```bash
   kubectl get pods -n genai-platform
   ```
   Should show both old and new version pods during canary.

3. Check service traffic:
   ```bash
   kubectl describe service genai-api -n genai-platform
   ```

## Troubleshooting

- **Rollout not starting**: Ensure Rollout CR is applied and image tag changed
- **Traffic not shifting**: Check service selector matches rollout labels
- **Promotion fails**: Verify analysis templates (added in next lab)

## What Just Happened?

You replaced your Deployment with a Rollout CR that implements canary deployment. Traffic gradually shifts from the stable version to the new version, allowing you to monitor for issues before full deployment.

## Challenge Exercise

Modify the canary steps in `rollout.yaml` to use different percentages (10%, 30%, 60%, 100%) and pause durations. Redeploy and observe the changes.