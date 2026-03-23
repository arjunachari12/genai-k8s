# 07: Prometheus Analysis for Rollout Validation

## Objective

Integrate Prometheus metrics into your canary rollout to automatically validate deployment success based on application metrics.

## Prerequisites

- Argo Rollouts Rollout deployed (from Lab 06)
- Prometheus running in cluster (from your monitoring setup)

## Step-by-step Instructions

### 1. Verify Prometheus Access

Check if Prometheus is running:
```bash
kubectl get pods -n monitoring
```

If not running, apply your prometheus.yaml:
```bash
kubectl apply -f monitoring/prometheus.yaml
```

### 2. Create AnalysisTemplate

Apply the analysis template:
```bash
kubectl apply -f training/manifests/analysis-template.yaml
```

### 3. Update Rollout with Analysis

Modify your `rollout.yaml` to include analysis steps. Add to the strategy:

```yaml
analysis:
  templates:
  - templateName: success-rate
  args:
  - name: service-name
    value: genai-api
  - name: namespace
    value: genai-platform
```

Apply the updated rollout:
```bash
kubectl apply -f training/manifests/rollout.yaml
```

### 4. Deploy with Analysis

Change image tag to v3 and trigger rollout:
```yaml
# In values.yaml
api:
  image:
    tag: "v3"
```

### 5. Monitor Analysis

Watch the rollout with analysis:
```bash
kubectl argo rollouts get rollout genai-api -n genai-platform --watch
```

Check analysis runs:
```bash
kubectl get analysisruns -n genai-platform
```

## Expected Output

- Analysis runs during canary steps
- Rollout pauses if metrics fail success criteria
- Successful analysis allows promotion
- Failed analysis triggers rollback

## Validation Steps

1. Check analysis template:
   ```bash
   kubectl get analysistemplates -n genai-platform
   ```

2. Monitor analysis runs:
   ```bash
   kubectl describe analysisrun -n genai-platform
   ```

3. Verify Prometheus queries work:
   ```bash
   # Port-forward Prometheus and check queries
   kubectl port-forward svc/prometheus -n monitoring 9090:9090
   ```

## Troubleshooting

- **Analysis fails**: Check Prometheus metrics availability and query syntax
- **Rollout doesn't pause**: Ensure analysis is properly configured in rollout spec
- **Metrics not found**: Verify serviceMonitor or metric collection setup

## What Just Happened?

You integrated Prometheus metrics into your rollout process. Argo Rollouts now automatically validates deployment health using real application metrics before promoting the canary.

## Challenge Exercise

Create a second AnalysisTemplate that checks error rates. Modify the rollout to use both success rate and error rate analysis. What happens if one analysis fails?