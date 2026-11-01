# 01 · Repair the container image

- Build the supplied image and capture its observed failure before changing it.
- Diagnose each fault using relevant logs, process/user/file/network observations, or small experiments. Record evidence, your hypothesis, and how you verified it.
- Commit durable fixes to the image build inputs, rebuild with a new tag, and deploy the resulting image.
- Run the application as a non-root user with appropriately scoped file permissions. Running it as root, using privileged mode, or broadly setting permissions to `777` does not meet the requirement.
- Keep required behavior and health checks enabled. Manual edits inside a running container are useful for investigation; the submitted build and deployment must reproduce the final state.

Refer to the [runtime settings](06-application-reference.md#application-contract) when configuring the container.

---

[Exercise overview](README.md) · [Previous part](00-scenario.md) · [Next part](02-deploy-with-helm.md)
