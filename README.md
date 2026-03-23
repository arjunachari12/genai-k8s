# GenAI Platform on Kubernetes

This repository contains the training project for Module 1: build and containerize a GenAI application, push the images to Docker Hub, and deploy the stack manually to a KIND cluster.

It now also includes Module 4 assets for autoscaling with KEDA and Prometheus metrics, plus Module 5 assets for packaging the same application as a reusable Helm chart with environment-specific values.

- A browser-based UI
- A FastAPI backend
- A local Ollama model runtime

The project stays intentionally focused on the core platform flow: containerization, image publishing, Kubernetes Deployments, Services, Ingress, and accessing the running application.

## Project Layout

```text
genai-platform/
├── api/
├── helm/
├── k8s/
├── llm/
├── ui/
└── docker-compose.yaml
```

## Commands

### 1. Build Docker Images

```bash
cd /home/arjun/genai-k8s/genai-platform

docker build -t arjunachari12/genai-ui:1.0.0 ./ui
docker build -t arjunachari12/genai-api:1.0.0 ./api
docker build -t arjunachari12/genai-ollama:1.0.0 ./llm
```

### 2. Push to Docker Hub

```bash
docker login

docker push arjunachari12/genai-ui:1.0.0
docker push arjunachari12/genai-api:1.0.0
docker push arjunachari12/genai-ollama:1.0.0
```


### 4. Apply Kubernetes Manifests

```bash
kubectl apply -f k8s/namespaces.yaml

kubectl apply -f k8s/llm-deployment.yaml
kubectl apply -f k8s/llm-service.yaml

kubectl apply -f k8s/api-deployment.yaml
kubectl apply -f k8s/api-service.yaml

kubectl apply -f k8s/ui-deployment.yaml
kubectl apply -f k8s/ui-service.yaml

kubectl apply -f k8s/ingress.yaml
```

### 5. Check the Pods

```bash
kubectl get pods -n genai
kubectl get svc -n genai
```

Expected result after the images are pulled and the model starts:

- `ui` pod is `Running`
- `api` pod is `Running`
- `llm` pod is `Running`

### 6. Access the UI

For this KIND setup, the most reliable way to access the app from your machine is with port-forwarding:

```bash
kubectl -n genai port-forward svc/ui-service 8080:80
```

Then open:

```text
http://127.0.0.1:8080/
```

You can also test the UI health endpoint:

```bash
curl http://127.0.0.1:8080/healthz
```

### 7. Test the API Through the UI Service

With the same port-forward still running, test the full request path:

```bash
curl -X POST http://127.0.0.1:8080/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "product": "AI-powered coffee subscription",
    "audience": "busy engineering managers"
  }'
```

If everything is working, the response returns JSON with:

- `model`
- `prompt`
- `content`

### 8. Optional NodePort Access

The service is also created as a NodePort on `30080`, but whether `http://localhost:30080` works depends on how the KIND cluster was created. If your KIND config includes host port mappings, you can try:

```bash
curl http://localhost:30080/healthz
open http://localhost:30080
```

If that does not work, use the `kubectl port-forward` method above.

### Optional: Local Docker Compose Test

```bash
docker compose up --build
```

Then open `http://localhost:8080`.

## Module 4: Autoscaling with KEDA and Prometheus

The KEDA autoscaling workshop materials live in:

[MODULE4_AUTOSCALING_KEDA.md](/home/arjun/genai-k8s/MODULE4_AUTOSCALING_KEDA.md)

Students install Prometheus Adapter, create a latency recording rule, deploy KEDA, and scale the API from Prometheus-driven p95 latency.

## Module 5: Helm Chart Development

The reusable Helm chart lives at `genai-platform/helm/genai-platform`.

### Chart Structure

```text
genai-platform/helm/genai-platform/
├── Chart.yaml
├── values.yaml
├── values-staging.yaml
├── values-production.yaml
└── templates/
```

### Validate the Chart

```bash
helm lint genai-platform/helm/genai-platform

helm template genai genai-platform/helm/genai-platform \
  --namespace genai-staging \
  -f genai-platform/helm/genai-platform/values-staging.yaml
```

### Install for Staging

```bash
helm upgrade --install genai genai-platform/helm/genai-platform \
  --namespace genai-staging \
  --create-namespace \
  -f genai-platform/helm/genai-platform/values-staging.yaml
```

Check the release:

```bash
helm status genai -n genai-staging
kubectl get pods,svc -n genai-staging
```

### Upgrade the Release

Example: change the API log level during the upgrade:

```bash
helm upgrade genai genai-platform/helm/genai-platform \
  --namespace genai-staging \
  -f genai-platform/helm/genai-platform/values-staging.yaml \
  --set api.logLevel=WARNING
```

Review release history:

```bash
helm history genai -n genai-staging
```

### Roll Back

```bash
helm rollback genai 1 -n genai-staging
helm history genai -n genai-staging
```

### Production Values

The production override increases frontend and API replicas, uses a ClusterIP service for the UI, keeps ingress enabled, and raises resource requests for the Ollama runtime:

```bash
helm upgrade --install genai genai-platform/helm/genai-platform \
  --namespace genai-prod \
  --create-namespace \
  -f genai-platform/helm/genai-platform/values-production.yaml
```

For the full student walkthrough that installs Prometheus, Grafana, Loki, Promtail, and the GenAI Helm chart together, use [MODULE5_HELM_OBSERVABILITY_APP.md](/home/arjun/genai-k8s/MODULE5_HELM_OBSERVABILITY_APP.md#L1).
