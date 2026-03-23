# 03: Custom Latency Metric

## Objective

Create a Prometheus recording rule for API p95 latency, then expose it through Prometheus Adapter as a Kubernetes custom metric.

## Files Used In This Exercise

- [genai-api-podmonitor.yaml](/home/arjun/genai-k8s/training/module4-keda/manifests/genai-api-podmonitor.yaml)
- [genai-latency-rule.yaml](/home/arjun/genai-k8s/training/module4-keda/manifests/genai-latency-rule.yaml)

## Step-by-step Instructions

### 1. Ensure Prometheus is scraping the API pods

Apply the PodMonitor:

```bash
kubectl apply -f training/module4-keda/manifests/genai-api-podmonitor.yaml
```

Verify it:

```bash
kubectl get podmonitor -n genai-staging
```

### 2. Create the p95 latency recording rule

```bash
kubectl apply -f training/module4-keda/manifests/genai-latency-rule.yaml
```

Verify it:

```bash
kubectl get prometheusrule -n monitoring
```

### 3. Generate a few requests so the metric appears

Port-forward the UI or call the API service directly:

```bash
kubectl -n genai-staging port-forward svc/genai-genai-platform-ui 8080:80
```

In another terminal:

```bash
for i in $(seq 1 5); do
  curl -s -X POST http://127.0.0.1:8080/api/generate \
    -H "Content-Type: application/json" \
    -d '{
      "product": "Latency demo",
      "audience": "platform engineers"
    }' > /dev/null
done
```

### 4. Query the recorded metric in Prometheus

Port-forward Prometheus:

```bash
kubectl -n monitoring port-forward svc/observability-kube-prometh-prometheus 9090:9090
```

In the Prometheus UI, run:

```text
genai_api_latency_p95_seconds{namespace="genai-staging"}
```

### 5. Query the metric through Kubernetes

```bash
kubectl get --raw \
  "/apis/custom.metrics.k8s.io/v1beta1/namespaces/genai-staging/pods/*/genai_api_latency_p95_seconds" | jq
```

## Expected Outcome

- Prometheus scrapes the API pods
- Prometheus records `genai_api_latency_p95_seconds` for each API pod
- Prometheus Adapter exposes that metric through `custom.metrics.k8s.io`

## Troubleshooting

- If the metric is empty, wait 1 to 2 scrape intervals and send more traffic
- If the custom metrics query fails, make sure Exercise 1 completed successfully
- If the PodMonitor is ignored, confirm the `release: observability` label is present

## What Just Happened?

You turned raw histogram buckets into a reusable, human-friendly latency signal that Kubernetes tooling can consume.
