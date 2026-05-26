---
name: libfuzzer
description: >
  Coverage-guided fuzzer built into LLVM for C/C++ projects compiled with Clang.
---

# libFuzzer

In-process, coverage-guided fuzzer built into LLVM. The recommended starting point for fuzzing C/C++ projects due to its simplicity. Maintenance-only since late 2022, but widely supported and easy to set up.

Harnesses written for libFuzzer are compatible with AFL++, making it easy to upgrade later.

## Installation

```bash
# Ubuntu/Debian
apt install clang llvm

# macOS
brew install llvm

# Verify
clang++ --version
```

## Compilation

```bash
# Basic
clang++ -fsanitize=fuzzer,address -g -O2 harness.cc target.cc -o fuzz

# With UBSan
clang++ -fsanitize=fuzzer,address,undefined -g -O2 harness.cc target.cc -o fuzz
```

| Flag | Purpose |
|------|---------|
| `-fsanitize=fuzzer` | Link libFuzzer runtime + enable coverage instrumentation |
| `-fsanitize=fuzzer-no-link` | Instrument without linking (for libraries/object files) |
| `-g` | Debug symbols |
| `-O2` | Production optimization (recommended for fuzzing) |
| `-U_FORTIFY_SOURCE` | Disable fortification (can interfere with ASan) |

### Static Libraries

```bash
# Build library with instrumentation
export CC=clang CFLAGS="-fsanitize=fuzzer-no-link -fsanitize=address"
./configure --enable-shared=no && make

# Link harness
clang++ -fsanitize=fuzzer,address harness.cc libmylib.a -o fuzz
```

### CMake

```cmake
add_executable(fuzz main.cc harness.cc)
target_compile_definitions(fuzz PRIVATE NO_MAIN=1)
target_compile_options(fuzz PRIVATE -g -O2 -fsanitize=fuzzer -fsanitize=address)
target_link_libraries(fuzz -fsanitize=fuzzer -fsanitize=address)
```

## Running

```bash
# Basic
./fuzz corpus/

# Continue after crashes (recommended)
./fuzz -fork=1 -ignore_crashes=1 corpus/

# Multi-core
./fuzz -jobs=4 -workers=4 -fork=1 -ignore_crashes=1 corpus/
```

### Common Options

| Option | Purpose |
|--------|---------|
| `-max_len=4000` | Max input size (rule of thumb: 2x minimal valid input) |
| `-timeout=2` | Abort test cases longer than N seconds |
| `-dict=./format.dict` | Use dictionary |
| `-close_fd_mask=3` | Close stdout/stderr (speed boost) |
| `-fork=N` | Fork mode with N processes |
| `-runs=0` | Test corpus without fuzzing |
| `-seed=N` | Reproduce a campaign (single-core only) |

### Interpreting Output

```text
#2      INITED cov: 3 ft: 4 corp: 1/1b exec/s: 0 rss: 26Mb
#57     NEW    cov: 4 ft: 5 corp: 2/4b lim: 4 exec/s: 0 rss: 26Mb
```

| Output | Meaning |
|--------|---------|
| `INITED` | Fuzzing initialized |
| `NEW` | New coverage found, input added to corpus |
| `REDUCE` | Input minimized while keeping coverage |
| `cov: N` | Coverage edges hit |
| `exec/s: N` | Executions per second |

On crash, the input is saved to `./crash-<hash>`.

## FuzzedDataProvider

For APIs needing structured input (multiple parameters, strings):

```c++
#include "FuzzedDataProvider.h"

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    FuzzedDataProvider fdp(data, size);
    auto alloc = fdp.ConsumeIntegral<size_t>();
    auto str = fdp.ConsumeBytesWithTerminator<char>(32, 0xFF);
    target(&str[0], str.size(), alloc);
    return 0;
}
```

Download from the [LLVM repository](https://github.com/llvm/llvm-project/blob/main/compiler-rt/include/fuzzer/FuzzedDataProvider.h).

## Custom Mutators

```c++
extern "C" size_t LLVMFuzzerCustomMutator(uint8_t *Data, size_t Size,
                                          size_t MaxSize, unsigned int Seed) {
    // Custom mutation logic
    return new_size;
}
```

## Real-World Example: libpng

```bash
# Get source
curl -L -O https://downloads.sourceforge.net/project/libpng/libpng16/1.6.37/libpng-1.6.37.tar.xz
tar xf libpng-1.6.37.tar.xz && cd libpng-1.6.37/
apt install zlib1g-dev

# Build with instrumentation
export CC=clang CFLAGS="-fsanitize=fuzzer-no-link -fsanitize=address"
export CXX=clang++ CXXFLAGS="$CFLAGS"
./configure --enable-shared=no && make

# Get harness, corpus, dictionary
curl -O https://raw.githubusercontent.com/glennrp/libpng/f8e5fa92b0e37ab597616f554bee254157998227/contrib/oss-fuzz/libpng_read_fuzzer.cc
mkdir corpus/ && curl -o corpus/input.png https://raw.githubusercontent.com/glennrp/libpng/acfd50ae0ba3198ad734e5d4dec2b05341e50924/contrib/pngsuite/iftp1n3p08.png
curl -O https://raw.githubusercontent.com/glennrp/libpng/2fff013a6935967960a5ae626fc21432807933dd/contrib/oss-fuzz/png.dict

# Link and fuzz
clang++ -fsanitize=fuzzer,address libpng_read_fuzzer.cc .libs/libpng16.a -lz -o fuzz
./fuzz -close_fd_mask=3 -dict=./png.dict corpus/
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No crashes after hours | Add seed inputs, use dictionary, check coverage |
| Very slow exec/sec (<100) | Use `-close_fd_mask=3`, reduce logging |
| Out of memory | Set `-rss_limit_mb=0` (ASan uses ~20TB virtual) |
| Stops after first crash | Use `-fork=1 -ignore_crashes=1` |
| Can't reproduce crash | Remove non-determinism (rand, global state) |
| GCC project won't compile | Switch to [AFL++](aflpp.md) with `gcc_plugin` |

## Resources

- [LLVM libFuzzer Documentation](https://llvm.org/docs/LibFuzzer.html)
- [libFuzzer Tutorial](https://github.com/google/fuzzing/blob/master/tutorial/libFuzzerTutorial.md)
- [SanitizerCoverage](https://clang.llvm.org/docs/SanitizerCoverage.html)
- [Structure-Aware Fuzzing](https://github.com/google/fuzzing/blob/master/docs/structure-aware-fuzzing.md)
