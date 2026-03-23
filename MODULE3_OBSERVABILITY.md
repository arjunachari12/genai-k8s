# Module 3: Observability with Prometheus, Loki, and Grafana

This module adds observability to the GenAI application without using Helm.

Students deploy the monitoring stack using plain Kubernetes manifests so they can understand the core building blocks before learning package-based installation later.

## Learning Goals

By the end of this module, students should be able to:

1. Deploy Prometheus using Kubernetes manifests
2. Expose FastAPI metrics and scrape them
3. Deploy Grafana and load starter dashboards
4. Deploy Loki and Promtail for log collection
5. Explore request count, latency, error rate, and logs

## Folder Structure

```text
genai-platform/
└── monitoring/
    ├── namespace.yaml
    ├── prometheus.yaml
    ├── grafana.yaml
    └── loki.yaml
```

## What Each Manifest Does

### `namespace.yaml`

Creates the `monitoring` namespace.

### `prometheus.yaml`

Deploys:

- a Prometheus configuration ConfigMap
- a Prometheus Deployment
- a Prometheus Service

Prometheus scrapes the FastAPI backend at:

`http://api-service.genai.svc.cluster.local:8000/metrics`

### `grafana.yaml`

Deploys:

- Grafana
- Prometheus and Loki data sources
- a starter dashboard

The dashboard includes:

- request count
- latency (p95)
- error rate
- API logs from Loki

### `loki.yaml`

Deploys:

- Loki
- Promtail
- Promtail RBAC resources

Promtail runs as a DaemonSet and collects pod logs from Kubernetes nodes.

## FastAPI Metrics

The FastAPI app already exposes Prometheus metrics.

This is enabled in:

[main.py](/home/arjun/genai-k8s/genai-platform/api/app/main.py)

The key line is:

`Instrumentator(excluded_handlers=["/health"]).instrument(app).expose(app)`

That exposes a `/metrics` endpoint which Prometheus scrapes.

## Deployment Order

Apply the monitoring manifests in this order:

```bash
kubectl apply -f genai-platform/monitoring/namespace.yaml
kubectl apply -f genai-platform/monitoring/prometheus.yaml
kubectl apply -f genai-platform/monitoring/loki.yaml
kubectl apply -f genai-platform/monitoring/grafana.yaml
```

## How to Verify

Check monitoring pods:

```bash
kubectl get pods -n monitoring
```

Check the application metrics endpoint from inside the cluster:

```bash
kubectl exec -n genai deploy/api -- wget -qO- http://127.0.0.1:8000/metrics | head
```

Port-forward Grafana:

```bash
kubectl -n monitoring port-forward svc/grafana 3000:3000
```

Open:

```text
http://127.0.0.1:3000
```

Default Grafana credentials:

- username: `admin`
- password: `admin123`

## Suggested Dashboard Discussion Points

Students can use the dashboard to answer questions like:

1. How many requests per second is the API serving?
2. What is the p95 latency?
3. Are there any 5xx errors?
4. What do the API logs show during failures or timeouts?

## Note on Traces

This module uses Prometheus, Grafana, Loki, and Promtail.

That gives us metrics and logs. For true distributed tracing, teams usually add a tracing backend such as Tempo or Jaeger. You can mention that in class as the next evolution of the platform, while still using this module for practical request analysis through metrics and logs.
