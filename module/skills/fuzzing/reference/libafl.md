---
name: libafl
description: >
  Modular Rust fuzzing library for building custom fuzzers or as a libFuzzer drop-in.
---

# LibAFL

Modular fuzzing library implementing AFL-style features as composable Rust components. Use as a drop-in libFuzzer replacement or build fully custom fuzzers from scratch.

**Choose LibAFL when** you need custom mutation strategies, non-standard target architectures, or fine-grained control over fuzzing components.

## Installation

```bash
# Install Clang 15-18
apt install clang

# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustup toolchain install nightly --component llvm-tools

# Configure environment
export RUSTFLAGS="-C linker=/usr/bin/clang"
export CC="clang" CXX="clang++"

# Additional dependencies
apt install libssl-dev pkg-config
```

## Usage Mode 1: libFuzzer Drop-in

Build LibAFL's compatibility layer and use existing libFuzzer harnesses:

```bash
git clone https://github.com/AFLplusplus/LibAFL
cd LibAFL/libafl_libfuzzer_runtime && ./build.sh

# Compile harness
clang++ -DNO_MAIN -g -O2 -fsanitize=fuzzer-no-link libFuzzer.a harness.cc main.cc -o fuzz
./fuzz corpus/
```

## Usage Mode 2: Custom Fuzzer (Rust Library)

```bash
cargo init --lib my_fuzzer && cd my_fuzzer
cargo add libafl@0.13 libafl_targets@0.13 libafl_bolts@0.13 libafl_cc@0.13 \
  --features "libafl_targets@0.13/libfuzzer,libafl_targets@0.13/sancov_pcguard_hitcounts"
```

Add to `Cargo.toml`:

```toml
[lib]
crate-type = ["staticlib"]
```

### Fuzzer Components

| Component | Role |
|-----------|------|
| **Observers** | Collect execution feedback (coverage, timing) |
| **Feedback** | Determine if inputs are interesting |
| **Objective** | Define goals (crashes, timeouts) |
| **State** | Maintain corpus and metadata |
| **Mutators** | Generate new inputs |
| **Scheduler** | Select inputs to mutate |
| **Executor** | Run the target |

### Basic Fuzzer Structure

```rust
use libafl::prelude::*;
use libafl_bolts::prelude::*;
use libafl_targets::{libfuzzer_test_one_input, std_edges_map_observer};

#[no_mangle]
pub extern "C" fn libafl_main() {
    let mut run_client = |state: Option<_>, mut mgr, _core_id| {
        let edges_observer = HitcountsMapObserver::new(
            unsafe { std_edges_map_observer("edges") }
        ).track_indices();
        let time_observer = TimeObserver::new("time");

        let mut feedback = feedback_or!(
            MaxMapFeedback::new(&edges_observer),
            TimeFeedback::new(&time_observer)
        );
        let mut objective = feedback_or_fast!(CrashFeedback::new(), TimeoutFeedback::new());

        let mut state = state.unwrap_or_else(|| {
            StdState::new(StdRand::new(), InMemoryCorpus::new(),
                OnDiskCorpus::new(&output_dir).unwrap(), &mut feedback, &mut objective).unwrap()
        });

        let mutator = StdScheduledMutator::new(havoc_mutations());
        let mut stages = tuple_list!(StdMutationalStage::new(mutator));
        let scheduler = IndexesLenTimeMinimizerScheduler::new(&edges_observer, QueueScheduler::new());
        let mut fuzzer = StdFuzzer::new(scheduler, feedback, objective);

        let mut harness = |input: &BytesInput| {
            libfuzzer_test_one_input(input.target_bytes().as_slice());
            ExitKind::Ok
        };
        let mut executor = InProcessExecutor::with_timeout(
            &mut harness, tuple_list!(edges_observer, time_observer),
            &mut fuzzer, &mut state, &mut mgr, timeout)?;

        if state.must_load_initial_inputs() {
            state.load_initial_inputs(&mut fuzzer, &mut executor, &mut mgr, &input_dir)?;
        }
        fuzzer.fuzz_loop(&mut stages, &mut executor, &mut state, &mut mgr)?;
        Ok(())
    };

    Launcher::builder().run_client(&mut run_client).cores(&cores).build().launch().unwrap();
}
```

## Compilation

### Compiler Wrapper (Recommended)

Create `src/bin/libafl_cc.rs`:

```rust
use libafl_cc::{ClangWrapper, CompilerWrapper, Configuration, ToolWrapper};

pub fn main() {
    let args: Vec<String> = env::args().collect();
    let mut cc = ClangWrapper::new();
    cc.cpp(is_cpp).parse_args(&args)
      .link_staticlib(&dir, "my_fuzzer")
      .add_args(&Configuration::GenerateCoverageMap.to_flags().unwrap())
      .add_args(&Configuration::AddressSanitizer.to_flags().unwrap())
      .run().unwrap();
}
```

```bash
cargo build --release
target/release/libafl_cxx -DNO_MAIN -g -O2 main.cc harness.cc -o fuzz
```

## Running

```bash
./fuzz --cores 0 --input corpus/              # Single core
./fuzz --cores 0,8-15 --input corpus/          # Multi-core
./fuzz -tui=1 corpus/                          # Text UI
```

## Advanced Features

### Crash Deduplication

```rust
let backtrace_observer = BacktraceObserver::owned("BacktraceObserver", HarnessType::InProcess);
let mut objective = feedback_and!(
    feedback_or_fast!(CrashFeedback::new(), TimeoutFeedback::new()),
    NewHashFeedback::new(&backtrace_observer)
);
```

### Dictionary / Auto Tokens

```rust
let mut tokens = Tokens::new();
tokens.add_from_file(tokenfile)?;
state.add_metadata(tokens);
let mutator = StdScheduledMutator::new(havoc_mutations().merge(tokens_mutations()));

// Auto tokens (enable in compiler wrapper)
cc.add_pass(LLVMPasses::AutoTokens);
tokens += libafl_targets::autotokens()?;
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No coverage increases | Verify compiler wrapper used, check `-fsanitize-coverage` |
| Linker errors with `libafl_main` | Use `-Wl,--whole-archive` or `-u libafl_main` |
| LLVM version mismatch | Install LLVM 15-18, set environment variables |
| Cannot attach debugger | Run in single-process mode (replace Launcher with SimpleEventManager) |

## Resources

- [LibAFL Book](https://aflplus.plus/libafl-book/)
- [LibAFL GitHub](https://github.com/AFLplusplus/LibAFL)
- [LibAFL API Docs](https://docs.rs/libafl/latest/libafl/)
- [LibAFL Examples](https://github.com/AFLplusplus/LibAFL/tree/main/fuzzers)
