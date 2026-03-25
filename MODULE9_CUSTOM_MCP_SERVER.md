# Module 9: Building and Deploying a Custom MCP Server

The Model Context Protocol (MCP) lets AI assistants call tools safely. In this module, you will deploy a small **read-only Kubernetes MCP server** inside your cluster so later modules can use live cluster data without giving the AI write access.

## 1. What the Server Exposes

Open `genai-platform/mcp-server/server.py`.

This server exposes these tools:

- `get_cluster_nodes`
- `get_namespaces`
- `get_pods_in_namespace`
- `get_recent_events`
- `get_pod_logs`

The goal is simple: give the AI enough visibility to inspect the cluster, but not enough permission to change it.

## 2. Review the RBAC

Open `genai-platform/mcp-server/k8s/rbac.yaml`.

Notice that the service account only has read permissions for:

- `nodes`
- `namespaces`
- `pods`
- `events`
- `pods/log`

This is an important design pattern for AI systems on Kubernetes:

- keep tool permissions narrow
- separate read tools from write actions
- make the AI safe by default

## 3. Build the Image

From the repository root:

```bash
cd /home/arjun/genai-k8s
docker build -t mcp-k8s-server:0.1.0 genai-platform/mcp-server
```

If you are using `kind`, load the image directly:

```bash
kind load docker-image mcp-k8s-server:0.1.0 --name multi-node-cluster
```

## 4. Deploy to Kubernetes

Apply the RBAC:

```bash
kubectl apply -f genai-platform/mcp-server/k8s/rbac.yaml
```

Deploy the server:

```bash
kubectl apply -f genai-platform/mcp-server/k8s/deployment.yaml
kubectl rollout status deployment/mcp-server -n genai
```

## 5. Test the Server

Port-forward the service:

```bash
kubectl port-forward -n genai svc/mcp-server-svc 8000:80
```

The MCP SSE endpoint will be:

```text
http://localhost:8000/sse
```

You can point an MCP-aware client at that URL, or use it in the next module when the LangGraph assistant connects to the cluster.

## Why This Matters

This MCP server is the bridge between:

- Kubernetes cluster state
- AI tools
- agent workflows

Without MCP, the model only sees a text prompt. With MCP, the model or agent can inspect real cluster context when it needs it.

## Summary

You now have a read-only Kubernetes MCP server deployed inside the cluster. In the next module, a LangGraph-based AI assistant will connect to this server, inspect unhealthy pods, and explain failures using a local Ollama model.
