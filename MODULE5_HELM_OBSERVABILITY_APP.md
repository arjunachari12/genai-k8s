# Module 5: Helm Observability and GenAI App Deployment

This guide shows one complete Helm-based flow for the same GenAI application:

1. Install observability into Kubernetes with Helm
2. Deploy the GenAI app with our Helm chart
3. Connect Prometheus to the app metrics endpoint
4. Install Loki for log collection
5. Verify the app and monitoring stack together

This walkthrough uses:

- `prometheus-community/kube-prometheus-stack` for Prometheus and Grafana
- `grafana/loki-stack` for Loki and Promtail
- our chart at `genai-platform/helm/genai-platform` for the GenAI app

## Prerequisites

- A working Kubernetes cluster such as KIND
- `kubectl` configured for that cluster
- `helm` installed
- Docker images for the app already pushed and reachable by the cluster

Check your tools:

```bash
kubectl config current-context
helm version
```

## Step 1: Add Helm Repositories

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

## Step 2: Install Prometheus and Grafana with Helm

Create a small values file for the monitoring stack:

```bash
cat <<'EOF' > /tmp/observability-values.yaml
grafana:
  adminUser: admin
  adminPassword: admin123
  additionalDataSources: []

prometheus:
  prometheusSpec:
    serviceMonitorSelectorNilUsesHelmValues: false
    podMonitorSelectorNilUsesHelmValues: false
    serviceMonitorNamespaceSelector: {}
    podMonitorNamespaceSelector: {}
EOF
```

Install the stack into the `monitoring` namespace:

```bash
helm upgrade --install observability prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  -f /tmp/observability-values.yaml
```

Verify the monitoring components:

```bash
kubectl get pods -n monitoring
kubectl get svc -n monitoring
helm status observability -n monitoring
```

## Step 3: Deploy the GenAI App with Our Helm Chart

The app chart lives here:

`genai-platform/helm/genai-platform`

For staging:

```bash
helm upgrade --install genai genai-platform/helm/genai-platform \
  --namespace genai-staging \
  --create-namespace \
  -f genai-platform/helm/genai-platform/values-staging.yaml
```

For production:

```bash
helm upgrade --install genai genai-platform/helm/genai-platform \
  --namespace genai-prod \
  --create-namespace \
  -f genai-platform/helm/genai-platform/values-production.yaml
```

Verify the app release:

```bash
helm status genai -n genai-staging
kubectl get pods,svc,pvc -n genai-staging
```

## Step 4: Expose App Metrics to Prometheus

Our FastAPI container already exposes `/metrics`, and the app chart already adds Prometheus annotations to the API pod template.

With `kube-prometheus-stack`, the cleanest way to scrape the API is a `PodMonitor`.

Apply this for staging:

```bash
kubectl apply -f - <<'EOF'
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: genai-api
  namespace: genai-staging
  labels:
    release: observability
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: genai-platform
      app.kubernetes.io/instance: genai
      app.kubernetes.io/component: api
  podMetricsEndpoints:
    - port: http
      path: /metrics
      interval: 15s
EOF
```

Check that the `PodMonitor` exists:

```bash
kubectl get podmonitor -n genai-staging
```

## Step 5: Install Loki and Promtail with Helm

Create a small values file for Loki:

```bash
cat <<'EOF' > /tmp/loki-stack-values.yaml
test_pod:
  enabled: false
loki:
  isDefault: false
  datasource:
    uid: loki
grafana:
  enabled: false
prometheus:
  enabled: false
fluent-bit:
  enabled: false
filebeat:
  enabled: false
logstash:
  enabled: false
EOF
```

Install Loki into the same `monitoring` namespace:

```bash
helm upgrade --install loki grafana/loki-stack \
  --namespace monitoring \
  -f /tmp/loki-stack-values.yaml
```

Verify the logging components:

```bash
kubectl get pods,svc -n monitoring | grep loki
helm status loki -n monitoring
```

Grafana needs to restart once so it reloads the new Loki datasource cleanly:

```bash
kubectl rollout restart deployment/observability-grafana -n monitoring
kubectl rollout status deployment/observability-grafana -n monitoring --timeout=180s
```

## Step 6: Open Grafana and Prometheus

Port-forward Grafana:

```bash
kubectl -n monitoring port-forward svc/observability-grafana 3000:80
```

Open:

```text
http://127.0.0.1:3000
```

Login with:

- username: `admin`
- password: `admin123`

Port-forward Prometheus:

```bash
kubectl -n monitoring port-forward svc/observability-kube-prometh-prometheus 9090:9090
```

Open:

```text
http://127.0.0.1:9090
```

## Step 7: Verify That Metrics and Logs Are Flowing

Generate a few requests against the UI:

```bash
kubectl -n genai-staging port-forward svc/genai-genai-platform-ui 8080:80
```

In another terminal:

```bash
curl http://127.0.0.1:8080/healthz

curl -X POST http://127.0.0.1:8080/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "product": "AI-powered coffee subscription",
    "audience": "busy engineering managers"
  }'
```

In Prometheus, check for metrics such as:

- `http_requests_total`
- `http_request_duration_seconds_bucket`

Example query:

```text
sum(rate(http_requests_total{handler!="/metrics"}[1m]))
```

In Grafana Explore, select the `Loki` datasource and run a query such as:

```text
{namespace="genai-staging",component="api"}
```

You should see API container logs such as:

- `GET /health`
- `GET /metrics`
- `HTTP Request: GET http://genai-genai-platform-llm.../api/tags`

## Step 8: Upgrade and Roll Back the App with Helm

Upgrade the staging release:

```bash
helm upgrade genai genai-platform/helm/genai-platform \
  --namespace genai-staging \
  -f genai-platform/helm/genai-platform/values-staging.yaml \
  --set api.logLevel=WARNING
```

Check history:

```bash
helm history genai -n genai-staging
```

Roll back:

```bash
helm rollback genai 1 -n genai-staging
helm history genai -n genai-staging
```

## What This Setup Gives You

- Prometheus installed with Helm
- Grafana installed with Helm
- Loki and Promtail installed with Helm
- The GenAI app installed with our own Helm chart
- Environment-specific values for staging and production
- A repeatable Helm workflow for install, upgrade, and rollback
- Live app metrics visible in Prometheus and Grafana
- Live app logs visible in Grafana through Loki

## Notes

- This document covers a practical Helm-based observability flow for metrics and logs.
- The repository still contains the manifest-based observability lab in `MODULE3_OBSERVABILITY.md`.
- The exact commands in this guide were verified against the local KIND setup in this repository.
- `grafana/loki-stack` is deprecated upstream, but it is kept here because it gives students a small, reliable local Loki setup for this workshop.
