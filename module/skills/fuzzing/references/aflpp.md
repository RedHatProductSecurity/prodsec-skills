---
name: aflpp
description: >
  AFL++ fork with multi-core support and advanced mutation strategies for C/C++ fuzzing.
---

# AFL++

Fork of AFL with better performance and stable multi-core support. The go-to fuzzer when you need parallel execution or your project requires GCC.

## Installation

| Method | When to Use |
|--------|-------------|
| Ubuntu/Debian repos | Recent Ubuntu, basic features |
| Docker (from Hub) | Specific version, Apple Silicon |
| From source | Need patches, avoid Docker |

```bash
# Ubuntu/Debian (check clang version with apt-cache show afl++)
apt install afl++ lld-17

# Docker
docker pull aflplusplus/aflplusplus:stable
```

### Wrapper Script

```bash
cat <<'EOF' > ./afl++
#!/bin/sh
AFL_VERSION="${AFL_VERSION:-"stable"}"
case "$1" in
   host) shift; bash -c "$*" ;;
   docker) shift; /usr/bin/env docker run -ti --privileged -v ./:/src --rm \
       --name afl_fuzzing "aflplusplus/aflplusplus:$AFL_VERSION" \
       bash -c "cd /src && bash -c \"$*\"" ;;
   *) echo "Usage: $0 {host|docker}"; exit 1 ;;
esac
EOF
chmod +x ./afl++
```

### System Configuration

```bash
./afl++ <host/docker> afl-system-config   # Run after each reboot, ~15% speedup
```

## Compilation

Choose mode by priority: **LTO** (`afl-clang-lto`) → **LLVM** (`afl-clang-fast`) → **GCC** (`afl-gcc-fast`).

```bash
# LLVM mode
./afl++ <host/docker> afl-clang-fast++ -DNO_MAIN=1 -O2 -fsanitize=fuzzer harness.cc main.cc -o fuzz

# GCC mode
./afl++ <host/docker> afl-g++-fast -DNO_MAIN=1 -O2 -fsanitize=fuzzer harness.cc main.cc -o fuzz

# With ASan
./afl++ <host/docker> AFL_USE_ASAN=1 afl-clang-fast++ -DNO_MAIN=1 -O2 -fsanitize=fuzzer harness.cc main.cc -o fuzz
```

## Running

```bash
# Basic
mkdir seeds && echo "aaaa" > seeds/minimal_seed
./afl++ <host/docker> afl-fuzz -i seeds -o out -- ./fuzz

# Multi-core (primary + secondaries)
./afl++ <host/docker> afl-fuzz -M primary -i seeds -o state -- ./fuzz &
./afl++ <host/docker> afl-fuzz -S secondary01 -i seeds -o state -- ./fuzz &
./afl++ <host/docker> afl-fuzz -S secondary02 -i seeds -o state -- ./fuzz &

# Monitor
./afl++ <host/docker> watch -n1 --color afl-whatsup state/
```

### Fuzzer Options

| Option | Purpose |
|--------|---------|
| `-G 4000` | Max input length (default: 1MB) |
| `-t 1000` | Timeout per test case in ms |
| `-x ./dict.dict` | Use dictionary |
| `-c0` | Enable CMPLOG (with CMPLOG-instrumented binary) |

### Input Modes

AFL++ supports libFuzzer-style harnesses, plus stdin and file modes:

```bash
# stdin fuzzing (no harness needed)
./afl++ <host/docker> afl-fuzz -i seeds -o out -- ./program

# File input (use @@ placeholder)
./afl++ <host/docker> afl-fuzz -i seeds -o out -- ./program @@
```

## Environment Variables

### Always Set

```bash
AFL_TMPDIR=/dev/shm  # Free performance win, saves SSD wear
```

### Slow Targets

```bash
AFL_FAST_CAL=1  # Speeds up calibration ~2.5x for targets >10ms/exec
```

### Multi-Core

```bash
AFL_FINAL_SYNC=1        # On primary only — needed for afl-cmin
AFL_TESTCACHE_SIZE=100  # Cache test cases in memory (MB, default 50)
```

### CI/Automated

```bash
AFL_EXIT_ON_TIME=3600   # Stop after 1 hour with no new paths
AFL_EXIT_WHEN_DONE=1    # Stop when all queue entries processed
AFL_NO_UI=1             # Headless
```

## CMPLOG

Best path constraint solver available. Build a CMPLOG-instrumented target:

```bash
./afl++ <host/docker> AFL_LLVM_CMPLOG=1 make
./afl++ <host/docker> afl-fuzz -c0 -S cmplog -i seeds -o state -- ./fuzz &
```

## Output Structure

```
out/default/
├── crashes/    # Crashing inputs
├── hangs/      # Hanging inputs
├── queue/      # Corpus (coverage-increasing inputs)
├── fuzzer_stats
└── plot_data
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Low exec/sec (<1k) | Create persistent-mode harness (`LLVMFuzzerTestOneInput`) |
| Low stability (<85%) | Fuzz via stdin/file instead of persistent mode |
| GCC plugin error | Ensure GCC version matches AFL++ build; install `gcc-N-plugin-dev` |
| No crashes found | Recompile with `AFL_USE_ASAN=1` |
| Memory limit exceeded (ASan) | Remove `-m` flag |

## Resources

- [AFL++ GitHub](https://github.com/AFLplusplus/AFLplusplus)
- [Fuzzing in Depth](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/refs/heads/stable/docs/fuzzing_in_depth.md)
- [AFL++ Under The Hood](https://blog.ritsec.club/posts/afl-under-hood/)
- [AFL++ Research Paper (USENIX)](https://www.usenix.org/system/files/woot20-paper-fioraldi.pdf)
- [Fuzzing cURL with AFL++](https://blog.trailofbits.com/2023/02/14/curl-audit-fuzzing-libcurl-command-line-interface/)
