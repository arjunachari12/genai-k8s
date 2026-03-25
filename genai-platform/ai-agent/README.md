# AI Kubernetes Assistant

This example packages a small LangGraph-based Kubernetes assistant that:

- uses a local Ollama model,
- calls Kubernetes read tools through an MCP server,
- runs inside a `kind` cluster as a simple Job or CronJob.

The assistant is intentionally small enough for students to read in one sitting.

## Components

- `agent.py`: LangGraph agent that plans, calls tools, and writes a short diagnosis.
- `k8s/ollama.yaml`: Runs Ollama inside the cluster and pre-pulls a small model.
- `k8s/job.yaml`: One-shot Job that asks the assistant to inspect the `genai` namespace.
- `k8s/cronjob.yaml`: Periodic health-check version of the same assistant.

## Local Build

```bash
cd /home/arjun/genai-k8s/genai-platform/ai-agent
docker build -t ai-k8s-assistant:0.1.0 .
kind load docker-image ai-k8s-assistant:0.1.0 --name multi-node-cluster
```

## Run In Cluster

```bash
kubectl apply -f /home/arjun/genai-k8s/genai-platform/ai-agent/k8s/ollama.yaml
kubectl apply -f /home/arjun/genai-k8s/genai-platform/mcp-server/k8s/rbac.yaml
kubectl apply -f /home/arjun/genai-k8s/genai-platform/mcp-server/k8s/deployment.yaml
kubectl apply -f /home/arjun/genai-k8s/genai-platform/ai-agent/k8s/job.yaml
```

Then follow the Job logs:

```bash
kubectl logs -n genai job/ai-k8s-assistant
```
