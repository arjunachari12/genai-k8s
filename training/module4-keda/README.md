# Module 4: Autoscaling with KEDA and Prometheus Metrics

## Overview

This module starts from the staging environment created in Module 5.

By the end of the labs, students will:

1. Install Prometheus Adapter
2. Install KEDA
3. Create a reusable p95 latency metric from Prometheus
4. Expose that metric through the Kubernetes custom metrics API
5. Scale the FastAPI API deployment when latency rises
6. Generate traffic and observe the scale-up and scale-down flow

## Prerequisites

- A running KIND cluster
- Module 5 completed in the `genai-staging` and `monitoring` namespaces
- `kubectl` configured for the cluster
- `helm` installed

Recommended validation before you begin:

```bash
kubectl get pods -n monitoring
kubectl get pods -n genai-staging
kubectl get podmonitor -A
```

## Module Structure

1. [01-prometheus-adapter-installation.md](01-prometheus-adapter-installation.md)
2. [02-keda-installation.md](02-keda-installation.md)
3. [03-custom-latency-metric.md](03-custom-latency-metric.md)
4. [04-latency-based-scaledobject.md](04-latency-based-scaledobject.md)
5. [05-traffic-simulation.md](05-traffic-simulation.md)

## Supporting Files

All manifests for this module live in:

[manifests/](/home/arjun/genai-k8s/training/module4-keda/manifests)
