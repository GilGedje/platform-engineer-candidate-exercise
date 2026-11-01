# 02 · Deploy with Helm

Your chart must deploy the application and either deploy or integrate PostgreSQL. Include:

- Application Deployment and Service, plus appropriate database resources.
- Configurable image repository/tag, resource requests/limits, and application settings.
- The required `APP_ENV` setting supplied at deployment time through a Helm value and container environment variable; use `local` for this exercise.
- Database credentials supplied through a Kubernetes Secret. Keep credentials out of the image and committed source. Document how to create the Secret from local inputs; do not submit live credentials.
- Suitable startup, readiness, and liveness behavior, with an explanation of what each check establishes.
- Persistent database storage and a documented storage-class assumption.
- Reproducible installation and upgrade instructions, including dependency versions and local image loading or registry setup.

Prove that you can change `APP_BUILD` through chart configuration and apply it with a Helm upgrade. Verify the result at `/version`. This configuration change is separate from the requirement to rebuild the repaired image.

Keep the [application settings and health endpoints](06-application-reference.md#application-contract) handy while writing your chart.

---

[Exercise overview](README.md) · [Previous part](01-repair-the-image.md) · [Next part](03-add-monitoring.md)
