# Module 4: Autoscaling with KEDA and Prometheus Metrics

This module builds on the Helm-based staging deployment and observability stack from Module 5.

Students will:

1. Install Prometheus Adapter for Kubernetes custom metrics exposure
2. Install KEDA for event-driven autoscaling
3. Create a custom latency metric from Prometheus data
4. Scale the FastAPI backend from that latency signal
5. Generate traffic and watch the autoscaler respond

The full step-by-step lab lives in:

[training/module4-keda/README.md](/home/arjun/genai-k8s/training/module4-keda/README.md)

The supporting manifests live in:

[training/module4-keda/manifests](/home/arjun/genai-k8s/training/module4-keda/manifests)
