# 00 · The scenario

## Your assignment

A developer has handed over a small Python application and its Dockerfile. The image builds, but the application does not operate correctly when deployed. Your task is to investigate, repair the image, write a Helm chart, and demonstrate a reliable local deployment with PostgreSQL and application monitoring.

We assess how you learn, gather evidence, explain decisions, and verify your work. Record what you already knew and what you learned during the exercise. Submit partial work and a clear explanation if you reach the time limit.

## What you receive

- A complete FastAPI application, Dockerfile, and pinned Python dependencies.
- A simple notes webpage at `/` for writing and reading notes, served by the same application container. The frontend is already supplied; no frontend development or build tool is required.
- An [application reference](06-application-reference.md) and acceptance criteria in the following parts.
- No Kubernetes manifests or Helm chart. You will create these.

The supplied Dockerfile contains deliberate runtime faults. Application features and instrumentation are already implemented; feature development is not required. You may make changes needed to operate the service, but preserve its API, PostgreSQL storage, and metrics behavior.

## Environment and scope

Use local Kubernetes: kind, Minikube, or Docker Desktop Kubernetes. A single-node cluster and one application replica are sufficient. Record your OS, CPU architecture, container runtime, Kubernetes, Helm, and other relevant tool versions.

Allow enough resources for Kubernetes, PostgreSQL, Prometheus, and Grafana. As an initial planning allowance, use 4 CPUs and 8 GiB available to the container runtime; actual use depends on your chosen setup. If hardware or image downloads prevent progress, contact the interviewer and document the issue.

Use an explicit image tag for your repaired application and explain how the cluster obtains that image. A public registry or cloud account is not required. Port forwarding is sufficient for local access. Keep the database internal to the cluster.

Use one replica of PostgreSQL with a PVC. Use a maintained PostgreSQL 17 image and record the exact version. You may write the database resources yourself or use a pinned Helm dependency. You must author the application Helm chart. Monitoring may be a separate Helm release.

---

[Exercise overview](README.md) · [Next part](01-repair-the-image.md)
