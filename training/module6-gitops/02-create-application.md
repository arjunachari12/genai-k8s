# 02: Creating ArgoCD Applications

## Objective

Create an ArgoCD Application that deploys your existing GenAI Helm chart, establishing GitOps control over your application.

## Prerequisites

- ArgoCD installed and running (from Lab 01)
- Your GenAI Helm chart in `genai-platform/helm/genai-platform/`
- Local directory initialized as a Git repository
- ArgoCD UI accessible

## Step-by-step Instructions

### 0. Initialize Local Git Repository (Required for ArgoCD)

ArgoCD requires a Git repository as the source, even for local development:

```bash
cd /home/arjun/genai-k8s
git init
git add .
git commit -m "Initial commit for ArgoCD"
```

### 1. Create ArgoCD Application via UI

1. Open ArgoCD UI at https://localhost:8080
2. Login with admin credentials
3. Click "New App"
4. Fill in the form:
   - **Application Name**: `genai-platform`
   - **Project**: `default`
   - **Sync Policy**: `Manual` (we'll change this later)
   - **Repository URL**: `file:///home/arjun/genai-k8s` (local Git repo)
   - **Path**: `genai-platform/helm/genai-platform`
   - **Cluster**: `https://kubernetes.default.svc` (in-cluster)
   - **Namespace**: `genai-platform` (or your app namespace)

### 2. Configure Helm Parameters

In the ArgoCD UI, under "Helm" tab:
- **Values Files**: `values.yaml`
- Add any custom values if needed

### 3. Sync the Application

1. Click "Create" to create the app
2. Click "Sync" to deploy
3. Monitor the sync process

### Alternative: Create via YAML

Apply the provided `argocd-app.yaml`:

```bash
kubectl apply -f training/manifests/argocd-app.yaml
```

## Expected Output

- ArgoCD Application created and synced
- Your GenAI application pods redeployed under ArgoCD control
- Application status shows "Synced" in ArgoCD UI

## Validation Steps

1. Check ArgoCD app status:
   ```bash
   kubectl get applications -n argocd
   ```

2. Verify pods are running:
   ```bash
   kubectl get pods -n genai-platform
   ```

3. Check ArgoCD UI for application health.

## Troubleshooting

- **Repository not accessible**: Ensure the path `genai-platform/helm/genai-platform` exists and you've initialized a Git repository in `/home/arjun/genai-k8s`
- **Helm chart errors**: Validate your Helm chart: `helm template genai-platform/helm/genai-platform/`
- **Sync fails**: Check ArgoCD logs: `kubectl logs -n argocd deployment/argocd-application-controller`
- **File URL not working**: ArgoCD requires a Git repository. Make sure you've run `git init` and `git add . && git commit` in the workspace root.

## What Just Happened?

You created an ArgoCD Application that connects your Git repository (local Helm chart) to your Kubernetes cluster. ArgoCD now manages the deployment lifecycle of your application.

## Challenge Exercise

Modify a value in your `values.yaml` file and sync the application. Observe how ArgoCD detects and applies the change.