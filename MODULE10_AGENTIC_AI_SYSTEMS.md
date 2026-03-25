# Module 10: Agentic AI Systems on Kubernetes

In Module 9, you connected AI tools to Kubernetes through MCP. In this module, you will deploy a small **AI Kubernetes assistant** inside your `kind` cluster.

This lab keeps the moving parts simple:

- **Ollama** runs the model locally
- a read-only **MCP server** exposes Kubernetes tools
- **LangGraph** drives the agent loop
- Kubernetes **Jobs** and **CronJobs** run the assistant

The result is similar in spirit to `kubectl-ai`, but the assistant runs inside the cluster and decides which tools to call before it answers.

## 1. Architecture

The assistant uses three components:

1. **Ollama**
   Runs a local model in the cluster. We use `tinyllama` to keep the workshop lightweight.

2. **MCP Server**
   Exposes read-only Kubernetes tools:
   - `get_pods_in_namespace`
   - `get_recent_events`
   - `get_pod_logs`

3. **LangGraph Assistant**
   Uses an agent loop to:
   - inspect the namespace
   - choose tools
   - summarize the issue
   - recommend a fix

## 2. Review the Code

Open these files:

- `genai-platform/mcp-server/server.py`
- `genai-platform/ai-agent/agent.py`

### MCP Server

The MCP server uses `FastMCP` and the Kubernetes Python client. It is intentionally read-only so students can focus on tool use without giving the AI permission to mutate the cluster.

### LangGraph Assistant

The assistant uses:

- `ChatOllama` for the local model
- `StateGraph` from LangGraph to model the investigation flow
- MCP-backed investigation steps that fetch pods, events, and logs

The flow is:

1. receive a question
2. inspect pods through MCP
3. branch to events and optional logs
4. print a short diagnosis

## 3. Build the Images

From the repository root:

```bash
cd /home/arjun/genai-k8s
docker build -t mcp-k8s-server:0.1.0 genai-platform/mcp-server
docker build -t ai-k8s-assistant:0.1.0 genai-platform/ai-agent
```

Load both into `kind`:

```bash
kind load docker-image mcp-k8s-server:0.1.0 --name multi-node-cluster
kind load docker-image ai-k8s-assistant:0.1.0 --name multi-node-cluster
```

## 4. Deploy the Stack

Deploy Ollama:

```bash
kubectl apply -f genai-platform/ai-agent/k8s/ollama.yaml
kubectl rollout status deployment/ollama -n genai --timeout=600s
```

Deploy the MCP server:

```bash
kubectl apply -f genai-platform/mcp-server/k8s/rbac.yaml
kubectl apply -f genai-platform/mcp-server/k8s/deployment.yaml
kubectl rollout status deployment/mcp-server -n genai
```

Run the assistant as a one-time Job:

```bash
kubectl apply -f genai-platform/ai-agent/k8s/job.yaml
```

Or run it every 15 minutes:

```bash
kubectl apply -f genai-platform/ai-agent/k8s/cronjob.yaml
```

## 5. Create a Failure for the Assistant

Create a broken deployment:

```bash
kubectl create deployment broken-redis \
  --image=redis:this-tag-does-not-exist \
  -n genai
```

Verify that the pod is unhealthy:

```bash
kubectl get pods -n genai
```

You should see `ImagePullBackOff` or `ErrImagePull`.

## 6. Observe the Agent

Read the Job logs:

```bash
kubectl logs -n genai job/ai-k8s-assistant
```

The output should show:

- the assistant prompt
- the tool calls chosen by the model
- tool results from MCP
- the final diagnosis

Expected outcome:

- the assistant identifies `broken-redis` as unhealthy
- it checks namespace events
- it explains that the image tag is invalid
- it suggests the next `kubectl` command or manifest fix

## 7. What Students Learn

This example demonstrates the core pieces of agentic AI on Kubernetes:

- **agent orchestration** with LangGraph
- **tool use** through MCP
- **local inference** with Ollama
- **safe Kubernetes access** with RBAC
- **Kubernetes-native execution** with Jobs and CronJobs

This is the same pattern you can expand later into:

- incident analysis agents
- rollout verifiers
- approval-based remediation
- self-healing operators

## 8. Cleanup

```bash
kubectl delete job ai-k8s-assistant -n genai --ignore-not-found
kubectl delete cronjob ai-k8s-assistant -n genai --ignore-not-found
kubectl delete deployment broken-redis -n genai --ignore-not-found
```

To remove the local AI stack:

```bash
kubectl delete -f genai-platform/ai-agent/k8s/ollama.yaml
kubectl delete -f genai-platform/mcp-server/k8s/deployment.yaml
kubectl delete -f genai-platform/mcp-server/k8s/rbac.yaml
```

## Summary

You now have a minimal **AI Kubernetes assistant** running in-cluster. It uses a local Ollama model, LangGraph for agent execution, and a read-only MCP server for live Kubernetes data. This gives students a clear, hands-on introduction to agentic AI without hiding the important implementation details.
