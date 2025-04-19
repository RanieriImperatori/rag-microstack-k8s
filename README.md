# RAG Microservices Stack on Kubernetes

This project implements a modular **Retrieval-Augmented Generation (RAG)** stack deployed as microservices on **Kubernetes**. It combines tools like **Qdrant**, **MinIO**, **Python-based services**, and **Ollama** as the LLM to demonstrate a scalable, production-ready architecture for building intelligent applications powered by large language models.

## 🚀 Overview

RAG (Retrieval-Augmented Generation) enhances language models with contextually relevant external knowledge. This stack demonstrates:

- **Data Ingestion and Chunking**
- **Embedding Generation**
- **Vector Search with Qdrant**
- **Object Storage via MinIO**
- **RAG API powered by FastAPI**
- **Deployment of Ollama as the LLM**
- **Containerized microservices on Kubernetes**
- **Deployment via ArgoCD (GitOps) on EKS**

## 🧱 Tech Stack

| Component        | Description                             |
|------------------|-----------------------------------------|
| **Python**       | Embedding, API, and data processing     |
| **Qdrant**       | Vector database for similarity search   |
| **MinIO**        | S3-compatible object storage            |
| **Ollama**       | LLM service for retrieval-augmented generation |
| **Kubernetes**   | Container orchestration (EKS/Minikube)    |
| **ArgoCD**       | GitOps-based deployment                 |
| **Helm**         | Package management for Kubernetes       |
| **Terraform**    | EKS provisioning and infrastructure     |

## 📂 Architecture

