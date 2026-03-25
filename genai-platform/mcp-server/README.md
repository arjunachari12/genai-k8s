# Kubernetes MCP Server

This example exposes a few **read-only Kubernetes tools** over MCP so an AI assistant can inspect cluster state safely.

## Tools

- `get_cluster_nodes`
- `get_namespaces`
- `get_pods_in_namespace`
- `get_recent_events`
- `get_pod_logs`

## Local Run

```bash
cd /home/arjun/genai-k8s/genai-platform/mcp-server
pip install -r requirements.txt
python server.py
```

The SSE endpoint is:

```text
http://localhost:8000/sse
```

## Build and Deploy to Kind

```bash
docker build -t mcp-k8s-server:0.1.0 .
kind load docker-image mcp-k8s-server:0.1.0 --name multi-node-cluster
kubectl apply -f k8s/rbac.yaml
kubectl apply -f k8s/deployment.yaml
```
