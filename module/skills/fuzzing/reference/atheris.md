---
name: atheris
description: >
  Coverage-guided Python fuzzer for pure Python code and C extensions.
---

# Atheris

Coverage-guided Python fuzzer built on libFuzzer. Fuzzes both pure Python code and Python C extensions with ASan support for detecting memory corruption.

## Installation

Supports 32/64-bit Linux and macOS. Fuzz on Linux for best results.

```bash
uv pip install atheris

# Verify
python -c "import atheris; print(atheris.__version__)"
```

### Docker Environment (Recommended for C Extensions)

```dockerfile
ARG PYTHON_VERSION=3.11
FROM python:$PYTHON_VERSION-slim-bookworm

RUN apt update && apt install -y ca-certificates wget && rm -rf /var/lib/apt/lists/*

ARG LLVM_VERSION=19
RUN echo "deb http://apt.llvm.org/bookworm/ llvm-toolchain-bookworm-$LLVM_VERSION main" > /etc/apt/sources.list.d/llvm.list \
    && wget -qO- https://apt.llvm.org/llvm-snapshot.gpg.key > /etc/apt/trusted.gpg.d/apt.llvm.org.asc \
    && apt update && apt install -y build-essential clang-$LLVM_VERSION && rm -rf /var/lib/apt/lists/*

ENV CC="clang-$LLVM_VERSION" CXX="clang++-$LLVM_VERSION"
ENV CFLAGS="-fsanitize=address,fuzzer-no-link" CXXFLAGS="-fsanitize=address,fuzzer-no-link"
ENV LDSHARED="clang-$LLVM_VERSION -shared" LDSHAREDXX="clang++-$LLVM_VERSION -shared"

RUN python -m venv /opt/venv && . /opt/venv/bin/activate
ENV PATH="/opt/venv/bin:$PATH"

RUN LIBFUZZER_LIB=$($CC -print-file-name=libclang_rt.fuzzer_no_main-$(uname -m).a) \
    python -m pip install --no-binary atheris atheris

ENV LD_PRELOAD="/opt/venv/lib/python3.11/site-packages/asan_with_fuzzer.so"
ENV ASAN_OPTIONS="allocator_may_return_null=1,detect_leaks=0"
```

## Fuzzing Pure Python

Use `instrument_imports()` to instrument all imported modules:

```python
import sys, atheris

with atheris.instrument_imports():
    import your_module

def test_one_input(data: bytes):
    try:
        your_module.parse(data)
    except ValueError:
        pass

atheris.Setup(sys.argv, test_one_input)
atheris.Fuzz()
```

**Instrumentation options:**
- `@atheris.instrument_func` — single function
- `atheris.instrument_imports()` — context manager for all imports
- `atheris.instrument_all()` — system-wide

## Fuzzing C Extensions

Install the extension from source with sanitizer flags:

```bash
MAKE="make --environment-overrides V=1" \
CC="/path/to/clang" CXX="/path/to/clang++" \
LDSHARED="/path/to/clang -shared" \
CFLAGS="-fsanitize=address,fuzzer-no-link -fno-omit-frame-pointer -fno-common -fPIC -g" \
    pip install --no-binary your_package your_package
```

Harness (no `@atheris.instrument_func` needed for C extensions):

```python
import sys, atheris
from _your_c_extension import parse

def test_one_input(data: bytes):
    try:
        parse(data)
    except Exception:
        pass

atheris.Setup(sys.argv, test_one_input)
atheris.Fuzz()
```

Run with LD_PRELOAD (don't export — set inline):

```bash
LD_PRELOAD=$(python -c 'import atheris, os; print(os.path.join(os.path.dirname(atheris.__file__), "asan_with_fuzzer.so"))') \
    python harness.py corpus/
```

## Running

```bash
python fuzz.py                         # Basic
python fuzz.py corpus/                 # With corpus
python fuzz.py -max_total_time=600     # 10 minute limit
python fuzz.py -max_len=1024           # Limit input size
python fuzz.py -workers=4 -jobs=4      # Parallel
```

All [libFuzzer options](https://llvm.org/docs/LibFuzzer.html#options) work as arguments.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No coverage increase | Verify `instrument_imports()` is used before imports |
| Import errors | Move imports inside `instrument_imports()` context |
| Segfault without ASan output | Set `LD_PRELOAD` to `asan_with_fuzzer.so` path |
| Slow execution | Reduce `max_len`, use `ASAN_OPTIONS=fast_unwind_on_malloc=1` |

## Resources

- [Atheris GitHub](https://github.com/google/atheris)
- [Native Extension Fuzzing Guide](https://github.com/google/atheris/blob/master/native_extension_fuzzing.md)
- [Continuously Fuzzing Python C Extensions](https://blog.trailofbits.com/2024/02/23/continuously-fuzzing-python-c-extensions/)
- [ClusterFuzzLite Python Integration](https://google.github.io/clusterfuzzlite/build-integration/python-lang/)
