# 03 · Add application monitoring

- Deploy Prometheus and Grafana using Helm. `prometheus-community/kube-prometheus-stack` is one suitable choice; pin the version you use.
- Configure Prometheus to scrape the supplied application's `/metrics` endpoint. Explain how your discovery configuration selects the application.
- Create and export a Grafana dashboard containing:
  - Application request rate, in requests per second.
  - HTTP error response percentage, including `4xx` and `5xx` responses; explain the definition and zero-traffic behavior.
  - Application p95 request duration, with correct units.
- Write a small traffic generator that produces successful requests and some expected error responses. Invalid note submissions can produce `422` responses without changing the application.
- Show that the Prometheus target is healthy and that dashboard values respond to traffic. Include the dashboard definition and the PromQL expressions in your submission.

Application metrics are required; generic Kubernetes dashboards alone do not satisfy this section. Alerting, logs aggregation, tracing, and PostgreSQL exporters are optional and are not needed for full marks.

Metric names and collection behavior are documented in the [application reference](06-application-reference.md#application-contract).

---

[Exercise overview](README.md) · [Previous part](02-deploy-with-helm.md) · [Next part](04-verify-recovery.md)
