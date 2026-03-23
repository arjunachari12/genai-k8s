# Project Overview

This repository contains a simple GenAI application designed for Kubernetes training.

The goal of the project is to help students understand how a small AI-powered application is structured before they write Kubernetes manifests for it.

## What This Project Does

The application generates short product messaging based on two inputs:

- `product`
- `audience`

A user enters those values in the UI. The backend turns them into a structured prompt and sends that prompt to a local large language model running with Ollama.

## High-Level Architecture

The application has three parts:

1. UI
2. API
3. LLM

Request flow:

`Browser -> UI -> API -> Ollama`

### UI

The UI is a small static web application.

It:

- shows a form
- collects user input
- sends a request to the backend
- displays the generated response

### API

The API is built with FastAPI.

It:

- exposes a `POST /generate` endpoint
- validates the request
- creates a clean prompt
- calls Ollama over HTTP
- returns structured JSON

### LLM

The LLM runtime uses Ollama with a lightweight model such as `tinyllama`.

It:

- starts the Ollama server
- pulls the model
- serves inference requests on port `11434`

## Repository Structure

```text
genai-platform/
├── api/
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── monitoring/
│   ├── grafana.yaml
│   ├── loki.yaml
│   ├── namespace.yaml
│   └── prometheus.yaml
├── llm/
│   ├── Dockerfile
│   └── entrypoint.sh
├── ui/
│   ├── Dockerfile
│   ├── default.conf.template
│   └── index.html
└── docker-compose.yaml
```

## Folder-by-Folder Explanation

### `genai-platform/ui`

This folder contains the frontend.

- `index.html`: the user interface and JavaScript logic
- `default.conf.template`: NGINX configuration that serves the UI and proxies `/api/` requests
- `Dockerfile`: builds the UI container image

### `genai-platform/api`

This folder contains the backend service.

- `app/main.py`: FastAPI application code
- `requirements.txt`: Python dependencies
- `Dockerfile`: builds the API container image

### `genai-platform/llm`

This folder contains the local model runtime setup.

- `entrypoint.sh`: starts Ollama and pulls the model
- `Dockerfile`: builds the Ollama-based container image

### `genai-platform/monitoring`

This folder contains the observability module manifests.

- `namespace.yaml`: creates the monitoring namespace
- `prometheus.yaml`: deploys Prometheus and configures scraping for the FastAPI metrics endpoint
- `grafana.yaml`: deploys Grafana with starter dashboards
- `loki.yaml`: deploys Loki and Promtail for cluster log collection

### `genai-platform/docker-compose.yaml`

This file is for local testing without Kubernetes.

It starts:

- the UI container
- the API container
- the Ollama container

## Key Learning Areas

This project is meant to teach students:

1. How a multi-container GenAI app is structured
2. How frontend, backend, and model runtime communicate
3. How to containerize each service
4. How to push images to Docker Hub
5. How to deploy the system to Kubernetes
6. How to observe the system with metrics and logs

## What Students Are Expected to Build

Students can use this repo as the application source and then create Kubernetes resources themselves.

Typical student tasks:

1. Write Deployments for UI, API, and LLM
2. Write Services for internal and external communication
3. Add Ingress if needed
4. Deploy the app to a Kubernetes cluster such as KIND
5. Test access to the UI and API

## End-to-End Flow

When the application runs:

1. The user opens the UI in a browser.
2. The user enters a product and audience.
3. The UI sends a request to the API.
4. The API builds a structured prompt.
5. The API calls Ollama.
6. Ollama runs the model and returns generated text.
7. The API sends the response back to the UI.
8. The UI displays the generated content.

## Why This Repo Is Useful For Training

This repo keeps the app simple while still showing realistic platform concepts:

- separate services
- Dockerfiles for each component
- environment-based configuration
- service-to-service communication
- local model inference

It is small enough to understand quickly, but complete enough to use in a real hands-on workshop.
