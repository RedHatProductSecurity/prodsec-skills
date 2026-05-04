---
name: build-yaml-misconfiguration
description: >
  Apply when reviewing or writing GitLab CI (.gitlab-ci.yml),
  Tekton pipeline/task YAML, or Containerfiles/Dockerfiles used in
  CI builds. Detects common misconfigurations that expose secrets,
  weaken isolation, skip security gates, grant excessive privileges,
  or produce insecure container images.
license: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)
origin: Adapted from CoSAI Project CodeGuard (https://github.com/cosai-oasis/project-codeguard)
category: "secure_development"
subcategory: "secure-config"
---

# Build YAML Misconfiguration

Detect and prevent security misconfigurations in GitLab CI and Tekton pipeline definitions. Misconfigured build YAML is a common source of secret leakage, privilege escalation, and supply chain compromise.

## GitLab CI (.gitlab-ci.yml)

### Secret Exposure

- **Never hardcode secrets** in `.gitlab-ci.yml`, `variables:`, or `script:` blocks. Use CI/CD protected variables or an external vault.
- **Mask and protect variables**: set `masked: true` and `protected: true` on sensitive CI/CD variables. Masked variables are redacted from job logs.
- **Never echo secrets**: avoid `echo $SECRET`, `printenv`, `env`, or `set -x` in scripts that handle credentials. Debug output is stored in job logs.
- **Restrict variable scope**: use `protected: true` to limit variables to protected branches/tags only. Use environment scoping to restrict which jobs see which secrets.
- **Artifacts and caches**: never include files containing secrets (`.env`, credentials, tokens) in `artifacts:` or `cache:` paths. These are stored and downloadable.

```yaml
# BAD -- secret visible in logs and available on all branches
variables:
  DB_PASSWORD: "hunter2"

# GOOD -- use CI/CD protected variable (set in GitLab UI)
# Reference as $DB_PASSWORD in scripts; set masked + protected in settings
```

### Runner and Execution Isolation

- **Never use shared runners for secret-heavy jobs** without understanding the trust boundary. Prefer project-specific or group runners for sensitive pipelines.
- **Never use `privileged: true`** in runner config unless absolutely required (e.g., container builds). Privileged runners can escape to the host.
- **Use `docker` or `kubernetes` executor** over `shell` executor. Shell executors share the host filesystem and can leak state between jobs.
- **Tag sensitive jobs** to run only on hardened, dedicated runners.

```yaml
# BAD -- no runner restriction, runs on any available shared runner
deploy-production:
  script:
    - ./deploy.sh

# GOOD -- pinned to a dedicated runner
deploy-production:
  tags:
    - production-deploy
    - privileged-denied
  script:
    - ./deploy.sh
```

### Pipeline Permissions and Trust

- **Protected branches**: ensure deploy and release jobs use `only: refs: [main]` or `rules:` with branch restrictions. Never allow feature branches to trigger production deploys.
- **Merge request pipelines**: use `rules: - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'` to prevent MR pipelines from accessing protected variables.
- **`allow_failure: true`**: never set this on security scanning jobs (SAST, SCA, secret detection). Failures in security gates must block the pipeline.
- **`when: manual`**: use for production deploys to enforce human approval. Never auto-deploy to production from CI.

```yaml
# BAD -- security scan can fail silently
sast:
  allow_failure: true
  script:
    - run-sast-scanner

# GOOD -- security scan blocks pipeline on failure
sast:
  allow_failure: false
  script:
    - run-sast-scanner
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
```

### Container Image Builds in CI

- **Never use `docker:dind` with `--privileged`** without understanding the risk. Prefer Kaniko, Buildah, or Podman for unprivileged image builds.
- **Pin base images by digest**, not just tag. Tags are mutable.
- **Do not mount the Docker socket** (`/var/run/docker.sock`) in CI jobs.
- **Scan built images** before pushing to registry.

```yaml
# BAD -- privileged DinD with mutable tag
build-image:
  image: docker:latest
  services:
    - docker:dind
  variables:
    DOCKER_HOST: tcp://docker:2375
  script:
    - docker build -t myapp .

# GOOD -- unprivileged build with pinned image
build-image:
  image: quay.io/buildah/stable@sha256:<digest>
  script:
    - buildah bud --layers -t myapp .
    - buildah push myapp $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

### Include and Extends Risks

- **Audit remote includes**: `include: remote:` pulls YAML from external URLs. If the remote changes, your pipeline changes. Pin to a specific ref or commit.
- **Audit cross-project includes**: `include: project:` pulls from other GitLab projects. Ensure the source project has proper access controls.
- **Review inherited configuration**: `extends:` and `include:` can override `variables:`, `script:`, and `rules:` in unexpected ways. Verify the final merged configuration.

```yaml
# RISKY -- remote include with no version pinning
include:
  - remote: 'https://example.com/ci-templates/build.yml'

# BETTER -- pinned project include
include:
  - project: 'my-group/ci-templates'
    ref: 'v2.1.0'
    file: '/templates/build.yml'
```

---

## Tekton Pipelines

### Secret Exposure

- **Never inline secrets** in Task or Pipeline YAML. Use Kubernetes Secrets referenced via `secretKeyRef` in `env:` or mounted as volumes.
- **Never log secrets in steps**: avoid `echo`, `printenv`, `cat` on mounted secret files in `script:` blocks. Tekton step logs are stored and accessible.
- **Workspace binding**: when binding secrets as workspaces, ensure the workspace is not shared with untrusted tasks in the same pipeline.
- **Results**: never write secrets to Tekton `results`. Results are stored in the TaskRun/PipelineRun status and visible to anyone with read access.

```yaml
# BAD -- secret hardcoded in task
steps:
  - name: deploy
    image: registry.redhat.io/ubi9/ubi-minimal
    script: |
      curl -H "Authorization: Bearer my-secret-token" https://api.example.com

# GOOD -- secret from Kubernetes Secret
steps:
  - name: deploy
    image: registry.redhat.io/ubi9/ubi-minimal
    env:
      - name: API_TOKEN
        valueFrom:
          secretKeyRef:
            name: deploy-creds
            key: token
    script: |
      curl -H "Authorization: Bearer $API_TOKEN" https://api.example.com
```

### Step Image Security

- **Pin images by digest**: never use `:latest` or mutable tags for step images. A compromised tag can inject malicious code into your pipeline.
- **Use trusted registries**: prefer `registry.redhat.io` or your internal registry. Avoid pulling from untrusted public registries in production pipelines.
- **Minimal images**: use UBI minimal or distroless images. Avoid full OS images with unnecessary tools that expand the attack surface.

```yaml
# BAD -- mutable tag from public registry
steps:
  - name: build
    image: ubuntu:latest

# GOOD -- pinned digest from trusted registry
steps:
  - name: build
    image: registry.redhat.io/ubi9/ubi-minimal@sha256:<digest>
```

### Task and Pipeline Permissions

- **Run steps as non-root**: set `securityContext.runAsNonRoot: true` and `runAsUser` on steps. Never run build steps as root unless absolutely required.
- **Drop capabilities**: set `securityContext.capabilities.drop: ["ALL"]` on step containers.
- **Do not use `privileged: true`** in step security contexts.
- **Service account scoping**: bind the minimum RBAC to the service account running the PipelineRun. Never use the `pipeline` service account with cluster-admin privileges.
- **Limit workspace access**: use `readOnly: true` on workspace bindings when the task only needs to read.

```yaml
# BAD -- running as root with no restrictions
steps:
  - name: build
    image: registry.redhat.io/ubi9/ubi-minimal
    script: |
      make build

# GOOD -- non-root with dropped capabilities
steps:
  - name: build
    image: registry.redhat.io/ubi9/ubi-minimal
    securityContext:
      runAsNonRoot: true
      runAsUser: 1001
      capabilities:
        drop: ["ALL"]
    script: |
      make build
```

### Pipeline Structure Risks

- **Untrusted task references**: `taskRef` with `resolver: bundles` or `resolver: git` can pull tasks from external sources. Pin to specific digests or commits.
- **Parameter injection**: if pipeline parameters are passed into `script:` blocks via `$(params.*)`, treat them as untrusted input. Validate and quote them.
- **When expressions**: do not use `when` expressions as security controls. They skip tasks but do not enforce authorization.
- **Finally tasks**: use `finally:` tasks for cleanup (removing credentials, revoking tokens) but never assume they will always run (node failure, timeout).

```yaml
# BAD -- unpinned external task bundle
taskRef:
  resolver: bundles
  params:
    - name: bundle
      value: quay.io/someone/my-task:latest

# GOOD -- pinned by digest
taskRef:
  resolver: bundles
  params:
    - name: bundle
      value: quay.io/myorg/my-task@sha256:<digest>
```

### Tekton Chains and Provenance

- **Enable Tekton Chains** for automatic signing and attestation of TaskRun/PipelineRun results.
- **Verify signatures** on built artifacts before promotion to production registries.
- **Store attestations** alongside artifacts for auditability.

---

## Containerfile / Dockerfile Hardening

Container image definitions are typically referenced or inlined in CI YAML. Misconfigurations here produce insecure images that run in production.

### Run as Non-Root

- **Never leave `USER` unset** -- the default is root. Always add a `USER` directive before the final `CMD`/`ENTRYPOINT`.
- Create a dedicated user in the build stage.

```dockerfile
# BAD -- runs as root by default
FROM registry.redhat.io/ubi9/ubi-minimal
COPY app /app
CMD ["/app/server"]

# GOOD -- explicit non-root user
FROM registry.redhat.io/ubi9/ubi-minimal
RUN microdnf install -y shadow-utils && \
    useradd -r -u 1001 appuser && \
    microdnf clean all
COPY --chown=appuser:appuser app /app
USER appuser
CMD ["/app/server"]
```

### Secrets in Image Layers

- **Never `COPY` or `ADD` secrets** (keys, credentials, `.env` files) into the image. Every layer is extractable.
- **Never use `ARG` or `ENV` for secrets** -- they are visible in `docker inspect` and image history.
- Use BuildKit secret mounts for build-time secrets. They are not persisted in layers.

```dockerfile
# BAD -- secret baked into image layer
COPY .env /app/.env
ENV API_KEY=sk-secret-value

# GOOD -- BuildKit secret mount (not persisted in layer)
RUN --mount=type=secret,id=api_key \
    export API_KEY=$(cat /run/secrets/api_key) && \
    ./configure --with-key="$API_KEY"
```

### Base Image Hygiene

- **Pin base images by digest**, not mutable tags. `:latest` or `:9` can change without notice.
- **Use trusted registries**: prefer `registry.redhat.io` or your internal registry.
- **Use minimal base images**: UBI minimal, micro, or distroless. Fewer packages = smaller attack surface.
- **Remove package managers** from the final image when possible.

```dockerfile
# BAD -- mutable tag, full OS image
FROM ubuntu:latest

# GOOD -- pinned digest, minimal trusted image
FROM registry.redhat.io/ubi9/ubi-minimal@sha256:<digest>
```

### Multi-Stage Builds

- **Separate build and runtime stages**. Build tools, compilers, and test dependencies must not ship in the final image.
- Copy only the built artifact into the runtime stage.

```dockerfile
# GOOD -- multi-stage: build tools stay in builder stage
FROM registry.redhat.io/ubi9/ubi:latest AS builder
RUN dnf install -y gcc make && dnf clean all
COPY . /src
RUN cd /src && make

FROM registry.redhat.io/ubi9/ubi-minimal@sha256:<digest>
COPY --from=builder /src/bin/app /app/server
USER 1001
CMD ["/app/server"]
```

### Build Context Leakage

- **Always use `.dockerignore`** (or `.containerignore`). Without it, the entire directory (including `.git`, `.env`, credentials, IDE configs) is sent to the build daemon.
- Explicitly exclude sensitive paths.

```text
# .dockerignore
.git
.env
*.pem
*.key
credentials/
node_modules/
```

### Unnecessary Capabilities and Ports

- **Do not `EXPOSE` ports you don't use**. While `EXPOSE` is documentation only, it signals intent and misconfigured orchestrators may open them.
- **Do not install `sudo`**, `su`, or setuid binaries in the final image.
- **Set `HEALTHCHECK`** so orchestrators can detect unhealthy containers.

```dockerfile
# GOOD -- only expose what's needed, add healthcheck
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8080/healthz || exit 1
```

### Read-Only and Immutability

- Design images to run with a **read-only root filesystem** at runtime. Write only to explicitly mounted volumes or `tmpfs`.
- Avoid writing to the container filesystem in `CMD`/`ENTRYPOINT` scripts.

### Common Containerfile Misconfigurations

| Misconfiguration | Risk | Fix |
|-----------------|------|-----|
| No `USER` directive | Container runs as root | Add `USER <non-root>` before CMD |
| `COPY .env` or `COPY *.key` | Secrets baked into extractable layers | Use BuildKit `--mount=type=secret` |
| `ENV SECRET_KEY=value` | Secret visible in `docker inspect` | Pass at runtime via orchestrator |
| `FROM image:latest` | Mutable tag; supply chain risk | Pin by `@sha256:<digest>` |
| No `.dockerignore` | `.git`, credentials sent to build context | Create `.dockerignore` with exclusions |
| Single-stage with build tools | Compilers, test deps ship to production | Use multi-stage builds |
| `RUN chmod 777` | World-writable files in image | Use specific permissions (`chmod 755`) |
| No `HEALTHCHECK` | Orchestrator cannot detect unhealthy state | Add `HEALTHCHECK` instruction |
| `sudo` or setuid binaries installed | Privilege escalation path | Remove from final image |

---

## Common Misconfigurations (Both Platforms)

| Misconfiguration | Risk | Fix |
|-----------------|------|-----|
| Hardcoded secrets in YAML | Credential leakage via repo access or logs | Use vault/CI variables/K8s Secrets |
| `allow_failure: true` on security jobs | Security findings silently ignored | Set `allow_failure: false` |
| Mutable image tags (`:latest`) | Supply chain compromise via tag poisoning | Pin by digest |
| Privileged containers/runners | Container escape to host | Use unprivileged builds (Buildah/Kaniko) |
| Unscoped variables/secrets | Secrets available to untrusted branches/jobs | Scope to protected branches/environments |
| Debug output (`set -x`, `printenv`) | Secrets printed to job logs | Remove debug flags; use masked variables |
| Unpinned remote includes/task refs | External changes alter your pipeline | Pin to version/commit/digest |
| Missing security scan gates | Vulnerable code reaches production | Add SAST/SCA/image scanning as blocking steps |
| Auto-deploy to production | No human review before deploy | Require manual approval gate |
| Shell executor (GitLab) | Job-to-job state leakage on shared host | Use Docker/Kubernetes executor |
| No `USER` in Containerfile | Container runs as root in production | Add non-root `USER` directive |
| Secrets in image layers | Credentials extractable from image | Use BuildKit secret mounts |
| No `.dockerignore` | Sensitive files leak into build context | Create `.dockerignore` with exclusions |
| Single-stage build | Build tools ship to production | Use multi-stage builds |

## Implementation Checklist

- [ ] No secrets hardcoded in pipeline YAML; all credentials from vault or protected variables
- [ ] Sensitive variables masked and scoped to protected branches/environments
- [ ] Security scan jobs set to block pipeline on failure
- [ ] All step/job images pinned by digest from trusted registries
- [ ] Containers run as non-root with dropped capabilities; no privileged mode
- [ ] Remote includes and task references pinned to specific versions/digests
- [ ] Production deploys require manual approval
- [ ] No debug output (`set -x`, `printenv`, `env`) in jobs that handle secrets
- [ ] Pipeline parameters validated before use in scripts
- [ ] Tekton Chains enabled for provenance and signing (where applicable)
- [ ] Containerfiles set explicit non-root `USER` before CMD
- [ ] No secrets in image layers, `ARG`, or `ENV`; use BuildKit secret mounts
- [ ] `.dockerignore` / `.containerignore` excludes `.git`, `.env`, keys, credentials
- [ ] Multi-stage builds separate build tools from runtime image
- [ ] Base images from trusted registries, pinned by digest

## Test Plan

- Audit all `.gitlab-ci.yml` and Tekton Task/Pipeline YAML for patterns in the table above.
- Verify that protected variables are not accessible from unprotected branches.
- Confirm security scan jobs block merge on failure.
- Test that pinned images resolve correctly and are from trusted registries.
- Review runner/service account RBAC for least privilege.
