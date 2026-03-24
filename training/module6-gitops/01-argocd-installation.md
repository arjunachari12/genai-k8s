# 01: ArgoCD Installation

## Objective

Install ArgoCD on your KIND cluster and confirm that both the UI and CLI are ready for the later GitOps exercises.

## Prerequisites

- KIND cluster running
- `kubectl` access to the cluster

## Step-by-step Instructions

### 1. Create the namespace

```bash
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -
```

### 2. Install ArgoCD

```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v2.10.0/manifests/install.yaml
kubectl wait --for=condition=Ready pod --all -n argocd --timeout=300s
```

This installs the ArgoCD API server, repo server, application controller, and supporting services into the `argocd` namespace.

### 3. Install the CLI

```bash
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
rm argocd-linux-amd64

argocd version --client
```

If you do not want to use `sudo`, install the binary into a directory that is already on your `PATH`, such as `/home/arjun/.local/bin`.

### 4. Access the UI

```bash
kubectl port-forward svc/argocd-server -n argocd 8081:443
```

### 5. Get the admin password

Username: `admin`

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

## Expected Output

- ArgoCD pods running in `argocd`
- UI available at `https://localhost:8081`
- Login works with `admin` and the initial password

## Validation Steps

1. Check pods:
   ```bash
   kubectl get pods -n argocd
   ```
2. Check the CLI:
   ```bash
   argocd version --client
   ```

## Troubleshooting

- If the namespace already exists, the `kubectl apply` pipeline keeps the command idempotent.
- If port `8081` is busy, use another local port such as `8082`.
- If CLI login later fails through port-forward, use `--grpc-web`.
- If pods are not ready, inspect logs with `kubectl logs -n argocd deployment/argocd-server`.

argocd app create guestbook \
  --repo https://github.com/argoproj/argocd-example-apps \
  --path guestbook \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default \
  --sync-policy automated \
  --auto-prune \
  --self-heal
