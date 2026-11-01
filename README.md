# Platform engineering take-home: repair, deploy, observe

**Level:** mid-level DevOps / platform engineer  
**Time budget:** up to two working days, with a maximum of 16 hours of active work  
**Follow-up:** a 60-minute technical discussion and practical walkthrough

## Scenario

A developer has handed over a small Python application and its Dockerfile. The image builds, but the application does not operate correctly when deployed. Your task is to investigate, repair the image, write a Helm chart, and demonstrate a reliable local deployment with PostgreSQL and application monitoring.

We assess how you learn, gather evidence, explain decisions, and verify your work. Record what you already knew and what you learned during the exercise. Submit partial work and a clear explanation if you reach the time limit.

## What you receive

- A complete FastAPI application, Dockerfile, and pinned Python dependencies.
- An application contract and acceptance criteria below.
- No Kubernetes manifests or Helm chart. You will create these.

The supplied Dockerfile contains deliberate runtime faults. Application features and instrumentation are already implemented; feature development is not required. You may make changes needed to operate the service, but preserve its API, PostgreSQL storage, and metrics behavior.

## Environment and scope

Use local Kubernetes: kind, Minikube, or Docker Desktop Kubernetes. A single-node cluster and one application replica are sufficient. Record your OS, CPU architecture, container runtime, Kubernetes, Helm, and other relevant tool versions.

Allow enough resources for Kubernetes, PostgreSQL, Prometheus, and Grafana. As an initial planning allowance, use 4 CPUs and 8 GiB available to the container runtime; actual use depends on your chosen setup. If hardware or image downloads prevent progress, contact the interviewer and document the issue.

Use an explicit image tag for your repaired application and explain how the cluster obtains that image. A public registry or cloud account is not required. Port forwarding is sufficient for local access. Keep the database internal to the cluster.

Use one replica of PostgreSQL with a PVC. Use a maintained PostgreSQL 17 image and record the exact version. You may write the database resources yourself or use a pinned Helm dependency. You must author the application Helm chart. Monitoring may be a separate Helm release.

## Required work

### 1. Investigate and repair the image

- Build the supplied image and capture its observed failure before changing it.
- Diagnose each fault using relevant logs, process/user/file/network observations, or small experiments. Record evidence, your hypothesis, and how you verified it.
- Commit durable fixes to the image build inputs, rebuild with a new tag, and deploy the resulting image.
- Run the application as a non-root user with appropriately scoped file permissions. Running it as root, using privileged mode, or broadly setting permissions to `777` does not meet the requirement.
- Keep required behavior and health checks enabled. Manual edits inside a running container are useful for investigation; the submitted build and deployment must reproduce the final state.

### 2. Author and deploy a Helm chart

Your chart must deploy the application and either deploy or integrate PostgreSQL. Include:

- Application Deployment and Service, plus appropriate database resources.
- Configurable image repository/tag, resource requests/limits, and application settings.
- The required `APP_ENV` setting supplied at deployment time through a Helm value and container environment variable; use `local` for this exercise.
- Database credentials supplied through a Kubernetes Secret. Keep credentials out of the image and committed source. Document how to create the Secret from local inputs; do not submit live credentials.
- Suitable startup, readiness, and liveness behavior, with an explanation of what each check establishes.
- Persistent database storage and a documented storage-class assumption.
- Reproducible installation and upgrade instructions, including dependency versions and local image loading or registry setup.

Prove that you can change `APP_BUILD` through chart configuration and apply it with a Helm upgrade. Verify the result at `/version`. This configuration change is separate from the requirement to rebuild the repaired image.

### 3. Add application monitoring

- Deploy Prometheus and Grafana using Helm. `prometheus-community/kube-prometheus-stack` is one suitable choice; pin the version you use.
- Configure Prometheus to scrape the supplied application's `/metrics` endpoint. Explain how your discovery configuration selects the application.
- Create and export a Grafana dashboard containing:
  - Application request rate, in requests per second.
  - HTTP error response percentage, including `4xx` and `5xx` responses; explain the definition and zero-traffic behavior.
  - Application p95 request duration, with correct units.
- Write a small traffic generator that produces successful requests and some expected error responses. Invalid note submissions can produce `422` responses without changing the application.
- Show that the Prometheus target is healthy and that dashboard values respond to traffic. Include the dashboard definition and the PromQL expressions in your submission.

Application metrics are required; generic Kubernetes dashboards alone do not satisfy this section. Alerting, logs aggregation, tracing, and PostgreSQL exporters are optional and are not needed for full marks.

### 4. Verify persistence and recovery

Record the commands and results for these checks:

1. Create a note, read it back, recreate the application pod, and read the same note again.
2. Recreate the PostgreSQL pod while preserving its PVC. Verify that the same note still exists.
3. Temporarily stop PostgreSQL in a controlled way, observe application behavior and health status, restore PostgreSQL, and verify recovery without rebuilding the application or deleting its data.
4. Apply a Helm upgrade changing `APP_BUILD`, and verify `/version` afterward.

Observe database-outage behavior through a direct application pod connection if necessary. Readiness can remove the application's endpoints from its Service during an outage, so distinguish an application HTTP response from a Service with no ready backend. Explain what the metrics can and cannot show in that situation.

## Application contract

The application listens on port `8000`. It uses one Uvicorn worker. Keep one worker for this exercise; the supplied in-process metrics do not configure multi-process aggregation.

**Required runtime configuration:** set `APP_ENV=local` for this exercise. `APP_ENV` has no default. An unset, empty, or whitespace-only value prevents startup with `APP_ENV is required`; unsupported values also prevent startup. Accepted values are `local`, `staging`, and `production`. The environment identifies the deployment in the startup record, startup log, and `/version` response.

Supply this variable through your Helm chart's runtime configuration. Keep it out of the Dockerfile's defaults, and preserve the startup validation. For a direct Docker investigation, pass `-e APP_ENV=local` to `docker run`. Setting it satisfies the documented configuration requirement; the supplied image still needs its runtime faults diagnosed and repaired.

| Setting | Default | Purpose |
|---|---|---|
| `APP_ENV` | **None — required** | Deployment environment; use `local` for this exercise |
| `DB_HOST` | `postgres` | PostgreSQL DNS name |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_NAME` | `notes` | Database name |
| `DB_USER` | `notes` | Database user |
| `DB_PASSWORD` | empty | Database password; supply through a Secret |
| `APP_STATE_DIR` | `/opt/notes/runtime` | Directory for a small per-process startup record; need not persist |
| `APP_BUILD` | `starter` | Build/deployment identifier exposed at `/version` |

The app creates its notes table automatically on the first successful database operation, including readiness checks. The database user needs permission to create that table. The application logs to standard output/error and does not log note contents or credentials. The startup record is local process metadata; notes are stored only in PostgreSQL.

| Method and endpoint | Behavior |
|---|---|
| `GET /livez` | `200` while the application can serve requests; independent of PostgreSQL |
| `GET /readyz` | `200` when database access works; `503` on database failure |
| `GET /version` | `200`, e.g. `{"build":"starter","environment":"local"}` |
| `POST /notes` | JSON `{"text":"hello"}`; returns `201` with `id`, `text`, `created_at` |
| `GET /notes` | `200` with up to 100 notes, newest first |
| `GET /notes/{id}` | `200` with a note, or `404` if absent |
| `GET /metrics` | Prometheus text exposition |
| `GET /docs` | Interactive API documentation |

Invalid note bodies return `422`. Database-dependent requests return `503` when the database is unavailable. Parameterized SQL is already implemented.

The supplied metrics are:

- `notes_http_requests_total{method,route,status}`
- `notes_http_request_duration_seconds_bucket{method,route,le}`, plus `_sum` and `_count`
- `notes_build_info{version}`
- Standard Python/process metrics

Health checks, metrics scrapes, and API documentation requests are excluded from the application HTTP counter and duration histogram. Dynamic note URLs use the route template `/notes/{note_id}` as their metric label.

Example API calls once your local access is configured:

```sh
curl -fsS http://127.0.0.1:8000/livez
curl -fsS http://127.0.0.1:8000/readyz
curl -fsS -H 'Content-Type: application/json' \
  -d '{"text":"hello from the exercise"}' http://127.0.0.1:8000/notes
curl -fsS http://127.0.0.1:8000/notes
```

## Submission

Submit a repository or archive with:

- Modified application/build inputs and your authored Helm chart.
- Monitoring configuration, exported dashboard, and traffic generator.
- Setup, install, upgrade, verification, and cleanup instructions that another engineer can follow from a clean cluster.
- A troubleshooting log: symptoms → evidence → hypotheses → fix → verification. Include at least one rejected hypothesis and the evidence that rejected it.
- A short learning note: prior familiarity, up to three things learned, useful documentation links, approximate active time by activity, and remaining limitations.
- Compact evidence of the acceptance checks. Screenshots can supplement commands and results. Remove passwords, tokens, and kubeconfigs from submitted evidence.

If working from the starter Git repository, preserve its initial commit and keep meaningful commits documenting your changes. Use a separate branch or your own repository for the solution. Submit access to a private repository or a Git bundle if sharing Git history; follow the interviewer's instructions for granting access.

Keep the written explanation focused; roughly 2–4 pages excluding setup commands and evidence is enough. The expected solution is a small local environment. CI/CD, GitOps, ingress/TLS, high availability, backups, and cloud deployment are outside the required scope and carry no additional points.

## Tools and assistance policy

Official documentation, ordinary web search, manuals, and existing technical articles are allowed. Attribute substantial copied snippets and adapt them to your solution.

AI assistance is excluded for this assessment. Do not use chat assistants, coding agents, generative autocomplete, generated search answers, or AI tools for code, configuration, debugging, explanations, or submission writing. Disable AI features in your editor and use search results that lead to documentation or articles. Ordinary non-generative editor completion is allowed.

You may ask the interviewer clarifying questions. If you accidentally receive AI assistance or are unsure whether a tool is permitted, disclose it and ask how to proceed before using its output.

## Assessment and follow-up

| Area | Weight |
|---|---:|
| Troubleshooting method and evidence | 30% |
| Linux/Docker understanding and durable image fixes | 25% |
| Kubernetes/Helm, configuration, and persistence | 20% |
| Application monitoring and verification | 15% |
| Reproducibility and explanation of learning | 10% |

In the follow-up, you will explain your solution, reproduce selected checks, and investigate one small change or fault with the interviewer. We will ask how you reached conclusions and what you would investigate next when evidence is incomplete.

## Useful starting documentation

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [kind quick start](https://kind.sigs.k8s.io/docs/user/quick-start/)
- [Helm documentation](https://helm.sh/docs/)
- [Kubernetes probes](https://kubernetes.io/docs/concepts/workloads/pods/probes/)
- [Kubernetes persistent volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [kube-prometheus-stack chart](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)
- [Prometheus Operator troubleshooting](https://prometheus-operator.dev/docs/platform/troubleshooting/)
- [Prometheus query functions](https://prometheus.io/docs/prometheus/latest/querying/functions/)
