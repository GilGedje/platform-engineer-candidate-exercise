# 05 · Submit your work

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

Technical verification may use automated checks. Troubleshooting method, learning, build provenance, and handoff quality are reviewed by the interviewer. Inaccessible infrastructure or an unsupported verification method needs follow-up rather than an automatic assumption about your skills.

---

[Exercise overview](README.md) · [Previous part](04-verify-recovery.md) · [Back to the app](../README.md)
