# 04 · Verify persistence and recovery

Record the commands and results for these checks:

1. Create a note, read it back, recreate the application pod, and read the same note again.
2. Recreate the PostgreSQL pod while preserving its PVC. Verify that the same note still exists.
3. Temporarily stop PostgreSQL in a controlled way, observe application behavior and health status, restore PostgreSQL, and verify recovery without rebuilding the application or deleting its data.
4. Apply a Helm upgrade changing `APP_BUILD`, and verify `/version` afterward.

Observe database-outage behavior through a direct application pod connection if necessary. Readiness can remove the application's endpoints from its Service during an outage, so distinguish an application HTTP response from a Service with no ready backend. Explain what the metrics can and cannot show in that situation.

---

[Exercise overview](README.md) · [Previous part](03-add-monitoring.md) · [Next part](05-submit-and-review.md)
