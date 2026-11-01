# Application reference

Use this page as a reference while working through the assignment.

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

Open `/` to use the notes webpage. Saving submits to the existing `POST /notes` endpoint; loading or refreshing the list reads `GET /notes`. Notes are stored in PostgreSQL, and the page confirms a save after the API succeeds. The browser does not store the notes in local storage. You may use the webpage or direct API calls to demonstrate the required persistence and recovery checks.

| Method and endpoint | Behavior |
|---|---|
| `GET /` | Notes webpage with a text box, Save note button, and saved notes list |
| `GET /static/{asset}` | Bundled frontend stylesheet, JavaScript, and favicon |
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

The HTTP metrics include webpage/asset requests as well as API traffic. Static asset paths share the bounded `/static` route label. Visiting and using the notes webpage therefore also generates observable application traffic.

Example API calls once your local access is configured:

```sh
curl -fsS http://127.0.0.1:8000/livez
curl -fsS http://127.0.0.1:8000/readyz
curl -fsS -H 'Content-Type: application/json' \
  -d '{"text":"hello from the exercise"}' http://127.0.0.1:8000/notes
curl -fsS http://127.0.0.1:8000/notes
```

## Useful starting documentation

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [kind quick start](https://kind.sigs.k8s.io/docs/user/quick-start/)
- [Helm documentation](https://helm.sh/docs/)
- [Kubernetes probes](https://kubernetes.io/docs/concepts/workloads/pods/probes/)
- [Kubernetes persistent volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [kube-prometheus-stack chart](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)
- [Prometheus Operator troubleshooting](https://prometheus-operator.dev/docs/platform/troubleshooting/)
- [Prometheus query functions](https://prometheus.io/docs/prometheus/latest/querying/functions/)

---

[Exercise overview](README.md) · [Previous part](05-submit-and-review.md) · [Back to the app](../README.md)
