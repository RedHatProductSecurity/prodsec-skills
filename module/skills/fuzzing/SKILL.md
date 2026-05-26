---
name: fuzzing
description: >
  Use when writing a fuzz harness, setting up a fuzzing campaign, integrating
  sanitizers, managing a corpus, or enrolling a project in continuous fuzzing for
  C/C++, Rust, Python, or Ruby.
license: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)
origin: Adapted from Trail of Bits Skills Marketplace (https://github.com/trailofbits/skills)
category: "security_testing"
subcategory: "fuzzing"
---

# Fuzzing

Coverage-guided fuzzing automatically generates inputs to find crashes, memory corruption, and undefined behavior. This skill detects your project's language and routes you to the right fuzzer.

## Pick a Fuzzer

### By Language

| Language | Default Fuzzer | When to Upgrade |
|----------|---------------|-----------------|
| **C/C++** | [libFuzzer](reference/libfuzzer.md) | Switch to [AFL++](reference/aflpp.md) for multi-core; [LibAFL](reference/libafl.md) for custom fuzzers |
| **Rust** | [cargo-fuzz](reference/cargo-fuzz.md) | Switch to [LibAFL](reference/libafl.md) for advanced research |
| **Python** | [Atheris](reference/atheris.md) | — |
| **Ruby** | [Ruzzy](reference/ruzzy.md) | — |

### By Need

| Need | Fuzzer |
|------|--------|
| Quick single-core C/C++ setup | [libFuzzer](reference/libfuzzer.md) |
| Multi-core C/C++ campaigns | [AFL++](reference/aflpp.md) |
| Custom mutators or research | [LibAFL](reference/libafl.md) |
| Cargo-based Rust project | [cargo-fuzz](reference/cargo-fuzz.md) |
| Python code or C extensions | [Atheris](reference/atheris.md) |
| Ruby code or C extensions | [Ruzzy](reference/ruzzy.md) |
| Continuous fuzzing for open source | [OSS-Fuzz](reference/ossfuzz.md) |

## Writing a Harness

The harness is the entry point that receives random bytes and calls your target code. Quality matters — a bad harness misses entire subsystems.

### Minimal Harnesses

**C/C++ (libFuzzer / AFL++):**

```c++
#include <stdint.h>
#include <stddef.h>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;
    target_function(data, size);
    return 0;
}
```

**Rust (cargo-fuzz):**

```rust
#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    if data.is_empty() { return; }
    your_crate::target_function(data);
});
```

**Python (Atheris):**

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

**Ruby (Ruzzy) — C extension:**

```ruby
require 'your_gem'
require 'ruzzy'

test_one_input = lambda do |data|
  begin
    YourGem.parse(data)
  rescue Exception
  end
  return 0
end

Ruzzy.fuzz(test_one_input)
```

### Harness Rules

| Do | Don't |
|----|-------|
| Handle all input sizes (empty, huge, malformed) | Call `exit()` — stops the fuzzer process |
| Join all threads before returning | Leave threads running between iterations |
| Keep harness fast (100s–1000s exec/sec) | Add logging or excessive I/O |
| Maintain determinism | Use `rand()`, `time()`, or `/dev/random` |
| Reset global state between runs | Rely on state from previous executions |
| Use narrow, focused targets | Mix unrelated formats in one harness |
| Free allocated resources | Create memory leaks |

### Structured Input

For APIs needing typed data, use `FuzzedDataProvider` (C/C++) or the `arbitrary` crate (Rust):

**C++ — FuzzedDataProvider:**

```c++
#include "FuzzedDataProvider.h"

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    FuzzedDataProvider fdp(data, size);
    auto len = fdp.ConsumeIntegral<size_t>();
    auto str = fdp.ConsumeRandomLengthString(256);
    target(str.c_str(), len);
    return 0;
}
```

**Rust — arbitrary crate:**

```rust
use arbitrary::Arbitrary;

#[derive(Debug, Arbitrary)]
pub struct Config { pub name: String, pub count: u32 }

fuzz_target!(|config: Config| { process(config); });
```

### Interleaved Fuzzing

Test multiple related operations in one harness by using the first byte as an operation selector:

```c++
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;
    switch (data[0] % 3) {
        case 0: parse(data + 1, size - 1); break;
        case 1: validate(data + 1, size - 1); break;
        case 2: transform(data + 1, size - 1); break;
    }
    return 0;
}
```

## Sanitizers

Sanitizers detect bugs that don't cause immediate crashes. **Always fuzz with at least AddressSanitizer enabled.**

### Quick Reference

| Sanitizer | Detects | Flag |
|-----------|---------|------|
| AddressSanitizer (ASan) | Buffer overflows, use-after-free, double-free | `-fsanitize=address` |
| UndefinedBehaviorSanitizer | Integer overflow, null deref, misaligned access | `-fsanitize=undefined` |
| MemorySanitizer | Uninitialized memory reads | `-fsanitize=memory` |

### By Fuzzer

| Fuzzer | How to Enable ASan |
|--------|-------------------|
| libFuzzer | `clang++ -fsanitize=fuzzer,address -g -O2 harness.cc -o fuzz` |
| AFL++ | `AFL_USE_ASAN=1 afl-clang-fast++ -fsanitize=fuzzer harness.cc -o fuzz` |
| cargo-fuzz | Enabled by default; `--sanitizer none` for safe Rust |
| Atheris | Set `CFLAGS="-fsanitize=address,fuzzer-no-link"` when installing C extensions |
| Ruzzy | `LD_PRELOAD=$(ruby -e 'require "ruzzy"; print Ruzzy::ASAN_PATH')` |

### Key ASan Options

```bash
ASAN_OPTIONS=verbosity=1:abort_on_error=1:detect_leaks=0
```

- `verbosity=1` — confirms ASan is active
- `abort_on_error=1` — some fuzzers need `abort()` not `_exit()`
- `detect_leaks=0` — disable during fuzzing (noisy)

ASan uses ~20TB virtual memory. Disable fuzzer memory limits: libFuzzer `-rss_limit_mb=0`, AFL++ `-m none`.

## Corpus Management

### Creating a Corpus

```bash
mkdir corpus/
# Add seed inputs — valid examples of the format you're fuzzing
cp test_data/*.bin corpus/
```

Seed inputs dramatically improve effectiveness — the fuzzer doesn't start from scratch.

### Minimization

```bash
# libFuzzer
mkdir minimized/ && ./fuzz -merge=1 minimized/ corpus/

# AFL++
afl-cmin -i out/default/queue -o minimized/ -- ./fuzz

# cargo-fuzz
cargo +nightly fuzz run target -- -merge=1 minimized/ corpus/
```

## Dictionaries

Dictionaries provide domain-specific tokens (magic bytes, keywords) to help fuzzers explore structured formats faster.

### Format

```conf
# dictionary.dict
magic="\x89PNG\r\n\x1a\n"
"GET"
"Content-Type"
kw="\xFF\xD8"
```

### Usage

| Fuzzer | Flag |
|--------|------|
| libFuzzer | `./fuzz -dict=./dict.dict corpus/` |
| AFL++ | `afl-fuzz -x ./dict.dict -i seeds -o out -- ./fuzz` |
| cargo-fuzz | `cargo fuzz run target -- -dict=./dict.dict` |

### Generation Methods

```bash
# From header files
grep -o '".*"' header.h > header.dict

# From binary strings
strings ./binary | sed 's/^/"&/; s/$/&"/' > strings.dict

# From AFL++ auto-extraction (compile-time)
AFL_LLVM_DICT2FILE=auto.dict afl-clang-lto++ target.cc -o target
```

Or prompt an LLM: *"Generate a libFuzzer dictionary for a PNG parser with magic bytes and chunk types."*

## Coverage Analysis

Use coverage to assess harness effectiveness and identify blockers.

### Quick Commands

| Toolchain | Build for Coverage | Generate Report |
|-----------|--------------------|-----------------|
| LLVM (C/C++) | `clang++ -fprofile-instr-generate -fcoverage-mapping ...` | `llvm-profdata merge -sparse *.profraw -o cov.profdata && llvm-cov show ./bin -instr-profile=cov.profdata -format=html -output-dir html/` |
| GCC (C/C++) | `g++ -ftest-coverage -fprofile-arcs ...` | `gcovr --html-details -o coverage.html` |
| cargo-fuzz (Rust) | `cargo +nightly fuzz coverage target` | Use `cargo cov -- show` with `-Xdemangler=rustfilt` |

Don't use `-fsanitize=fuzzer` for coverage builds — it conflicts with profile instrumentation.

## Overcoming Obstacles

Checksums, PRNGs, and complex validation block fuzzer progress. Use conditional compilation to bypass them during fuzzing while preserving production behavior.

**C/C++:**

```c++
if (checksum != expected) {
#ifndef FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION
    return -1;  // Only enforced in production
#endif
}
```

**Rust:**

```rust
if checksum != expected {
    if !cfg!(fuzzing) {
        return Err(ChecksumError);
    }
}
```

libFuzzer and AFL++ define `FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION` automatically. cargo-fuzz sets `cfg!(fuzzing)` automatically.

**Guidelines:**
- Keep cheap checks (magic bytes, size validation) — they guide the fuzzer
- Use fixed PRNG seeds during fuzzing for determinism
- Patch incrementally and measure coverage impact
- Provide safe defaults when skipping validation that downstream code depends on

## Resources

- [libFuzzer Documentation](https://llvm.org/docs/LibFuzzer.html)
- [AFL++ GitHub](https://github.com/AFLplusplus/AFLplusplus)
- [LibAFL Book](https://aflplus.plus/libafl-book/)
- [cargo-fuzz Book](https://rust-fuzz.github.io/book/cargo-fuzz.html)
- [Atheris GitHub](https://github.com/google/atheris)
- [Ruzzy GitHub](https://github.com/trailofbits/ruzzy)
- [OSS-Fuzz Documentation](https://google.github.io/oss-fuzz/)
- [Structure-Aware Fuzzing](https://github.com/google/fuzzing/blob/master/docs/structure-aware-fuzzing.md)
- [FuzzedDataProvider Header](https://github.com/llvm/llvm-project/blob/main/compiler-rt/include/fuzzer/FuzzedDataProvider.h)
