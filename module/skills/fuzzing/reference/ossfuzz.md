---
name: ossfuzz
description: >
  Free continuous fuzzing infrastructure for open-source projects by Google.
---

# OSS-Fuzz

Free continuous fuzzing infrastructure for open-source projects by Google. Provides distributed fuzzing, coverage reports, and bug tracking. The core is open-source — you can host your own instance for private projects.

## Quick Reference

| Task | Command |
|------|---------|
| Clone | `git clone https://github.com/google/oss-fuzz` |
| Build image | `python3 infra/helper.py build_image --pull <project>` |
| Build fuzzers | `python3 infra/helper.py build_fuzzers --sanitizer=address <project>` |
| Run fuzzer | `python3 infra/helper.py run_fuzzer <project> <harness>` |
| Coverage report | `python3 infra/helper.py coverage <project>` |

## Running Locally

```bash
git clone https://github.com/google/oss-fuzz && cd oss-fuzz

# Build and run (example: irssi)
python3 infra/helper.py build_image --pull irssi
python3 infra/helper.py build_fuzzers --sanitizer=address irssi
python3 infra/helper.py run_fuzzer irssi irssi-fuzz
```

The helper script auto-runs missed steps if you skip them.

### Coverage

```bash
# Install gsutil first: https://cloud.google.com/storage/docs/gsutil_install
python3 infra/helper.py build_fuzzers --sanitizer=coverage <project>
python3 infra/helper.py coverage <project>
```

## Enrolling a Project

Create three files in `projects/<your-project>/`:

### project.yaml

```yaml
homepage: "https://github.com/yourorg/yourproject"
language: c++    # c, c++, rust, python, go, java, swift
primary_contact: "your-email@example.com"
main_repo: "https://github.com/yourorg/yourproject"
fuzzing_engines:
  - libfuzzer
  - afl
sanitizers:
  - address
  - undefined
```

### Dockerfile

```dockerfile
FROM gcr.io/oss-fuzz-base/base-builder
RUN apt-get update && apt-get install -y autoconf automake libtool pkg-config
RUN git clone --depth 1 https://github.com/yourorg/yourproject
WORKDIR yourproject
COPY build.sh $SRC/
```

### build.sh

```bash
#!/bin/bash -eu
./autogen.sh && ./configure --disable-shared && make -j$(nproc)

$CXX $CXXFLAGS -std=c++11 -I. \
    $SRC/yourproject/fuzz/harness.cc -o $OUT/harness \
    $LIB_FUZZING_ENGINE ./libyourproject.a

cp $SRC/yourproject/fuzz/corpus.zip $OUT/harness_seed_corpus.zip
cp $SRC/yourproject/fuzz/dictionary.dict $OUT/harness.dict
```

Use `$LIB_FUZZING_ENGINE` — OSS-Fuzz handles engine-specific flags automatically.

## Language-Specific Integration

### Python (Atheris)

```python
import atheris, sys

@atheris.instrument_func
def TestOneInput(data):
    try:
        your_module.parse(data)
    except (ValueError, Exception):
        pass

atheris.Setup(sys.argv, TestOneInput)
atheris.Fuzz()
```

**build.sh:**

```bash
pip3 install .
for fuzzer in $(find $SRC -name 'fuzz_*.py'); do
    compile_python_fuzzer $fuzzer
done
```

### Rust (cargo-fuzz)

```yaml
# project.yaml
language: rust
sanitizers:
  - address  # Only ASan supported for Rust
```

**build.sh:**

```bash
cargo fuzz build -O --debug-assertions
cp fuzz/target/x86_64-unknown-linux-gnu/release/fuzz_target_1 $OUT/
```

## Web Tools

| Tool | URL | Purpose |
|------|-----|---------|
| Bug tracker | [issues.oss-fuzz.com](https://issues.oss-fuzz.com/issues?q=status:open) | Search bugs across all projects |
| Build status | [Build logs](https://oss-fuzz-build-logs.storage.googleapis.com/index.html) | Track build successes/failures |
| Fuzz Introspector | [Introspector](https://oss-fuzz-introspector.storage.googleapis.com/index.html) | Coverage data and blocker analysis |

## Docker Image Hierarchy

1. **base_image** → Ubuntu base
2. **base_clang** → Clang compiler
3. **base_builder** → Build dependencies (your Dockerfile extends this)
4. **base_runner** → Executes harnesses (separate from build)

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Build fails with missing deps | Add `apt-get install` in Dockerfile |
| Coverage is 0% | Verify harness calls target functions |
| Build timeout | Optimize build.sh, use parallel builds |
| Cannot find source | Set `WORKDIR` or use absolute paths in Dockerfile |

## Resources

- [OSS-Fuzz Documentation](https://google.github.io/oss-fuzz/)
- [Getting Started Guide](https://google.github.io/oss-fuzz/getting-started/accepting-new-projects/)
- [cbor2 Integration PR](https://github.com/google/oss-fuzz/pull/11444) (real-world Python example)
- [Fuzz Introspector Case Studies](https://github.com/ossf/fuzz-introspector/blob/main/doc/CaseStudies.md)
