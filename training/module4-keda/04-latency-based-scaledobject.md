# 04: Latency-Based ScaledObject

## Objective

Create a KEDA `ScaledObject` that increases API replicas when the p95 latency metric stays above the threshold.

## Files Used In This Exercise

- [keda-scaledobject.yaml](/home/arjun/genai-k8s/training/module4-keda/manifests/keda-scaledobject.yaml)

## Step-by-step Instructions

### 1. Inspect the current API replica count

```bash
kubectl get deployment genai-genai-platform-api -n genai-staging
```

### 2. Apply the ScaledObject

```bash
kubectl apply -f training/module4-keda/manifests/keda-scaledobject.yaml
```

### 3. Verify that KEDA created the HPA

```bash
kubectl get scaledobject -n genai-staging
kubectl get hpa -n genai-staging
kubectl describe scaledobject genai-api-latency -n genai-staging
```

### 4. Understand the threshold

This ScaledObject queries:

```text
avg(genai_api_latency_p95_seconds{namespace="genai-staging"})
```

It scales when the value rises above `1.5` seconds.

## Expected Outcome

- A `ScaledObject` named `genai-api-latency` exists
- KEDA creates an HPA for the API Deployment
- The Deployment is now managed by KEDA for replica changes

## Validation

```bash
kubectl get scaledobject genai-api-latency -n genai-staging -o yaml
kubectl get hpa -n genai-staging
```

## Troubleshooting

- If the HPA does not appear, inspect operator logs with `kubectl logs -n keda deployment/keda-operator`
- If the query returns no data, go back to Exercise 3 and confirm the recorded metric exists

## What Just Happened?

You connected a Prometheus latency query to a Kubernetes Deployment through KEDA. The next exercise will create traffic so that query crosses the scaling threshold.
