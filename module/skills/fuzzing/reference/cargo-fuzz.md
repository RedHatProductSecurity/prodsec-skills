---
name: cargo-fuzz
description: >
  De facto fuzzing tool for Rust projects using Cargo with libFuzzer backend.
---

# cargo-fuzz

The de facto fuzzing tool for Rust projects using Cargo. Uses libFuzzer as backend and provides a convenient Cargo subcommand with integrated sanitizer support.

## Installation

```bash
rustup install nightly
cargo install cargo-fuzz

# Verify
cargo +nightly --version && cargo fuzz --version
```

## Setup

Structure your code as a library crate (`src/lib.rs` with public functions). Then:

```bash
cargo fuzz init
# Creates fuzz/Cargo.toml and fuzz/fuzz_targets/fuzz_target_1.rs
```

Edit `fuzz/fuzz_targets/fuzz_target_1.rs`:

```rust
#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    if data.is_empty() { return; }
    your_crate::target_function(data);
});
```

## Structure-Aware Fuzzing

Use the `arbitrary` crate for automatic struct deserialization:

```rust
// In your library
use arbitrary::Arbitrary;

#[derive(Debug, Arbitrary)]
pub struct Config { pub name: String, pub count: u32 }
```

```rust
// In fuzz target
fuzz_target!(|config: your_crate::Config| {
    config.process();
});
```

Add to library's `Cargo.toml`:

```toml
[dependencies]
arbitrary = { version = "1", features = ["derive"] }
```

## Running

```bash
# Basic (ASan enabled by default)
cargo +nightly fuzz run fuzz_target_1

# Safe Rust only — disable sanitizers for 2x speed
cargo +nightly fuzz run --sanitizer none fuzz_target_1

# Check if your project uses unsafe
cargo install cargo-geiger && cargo geiger

# Re-run a crash
cargo +nightly fuzz run fuzz_target_1 fuzz/artifacts/fuzz_target_1/crash-<hash>

# Test corpus without fuzzing
cargo +nightly fuzz run fuzz_target_1 fuzz/corpus/fuzz_target_1 -- -runs=0
```

### libFuzzer Options

Pass after `--`:

```bash
cargo +nightly fuzz run fuzz_target_1 -- -help=1
cargo +nightly fuzz run fuzz_target_1 -- -timeout=10 -max_len=1024
cargo +nightly fuzz run fuzz_target_1 -- -dict=dict.dict
```

### Output Locations

- Corpus: `fuzz/corpus/fuzz_target_1/`
- Crashes: `fuzz/artifacts/fuzz_target_1/`

## Coverage Analysis

```bash
# Prerequisites
rustup toolchain install nightly --component llvm-tools-preview
cargo install cargo-binutils rustfilt

# Generate coverage
cargo +nightly fuzz coverage fuzz_target_1

# Create HTML report
TARGET=$(rustc -vV | sed -n 's|host: ||p')
cargo +nightly cov -- show -Xdemangler=rustfilt \
  "target/$TARGET/coverage/$TARGET/release/fuzz_target_1" \
  -instr-profile="fuzz/coverage/fuzz_target_1/coverage.profdata" \
  -show-line-counts-or-regions -show-instantiations \
  -format=html -o fuzz_html/ src/lib.rs
```

## Real-World Example: ogg Crate

```bash
git clone https://github.com/RustAudio/ogg.git && cd ogg/
cargo fuzz init
```

```rust
// fuzz/fuzz_targets/fuzz_target_1.rs
#![no_main]
use ogg::{PacketReader, PacketWriter};
use ogg::writing::PacketWriteEndInfo;
use std::io::Cursor;
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    let mut rdr = PacketReader::new(Cursor::new(data.to_vec()));
    rdr.delete_unread_packets();
    let mut wtr = PacketWriter::new(Cursor::new(Vec::new()));
    if let Ok(Some(pck)) = rdr.read_packet().and_then(|_| rdr.read_packet()) {
        let inf = if pck.last_in_stream() { PacketWriteEndInfo::EndStream }
                  else if pck.last_in_page() { PacketWriteEndInfo::EndPage }
                  else { PacketWriteEndInfo::NormalPacket };
        let _ = wtr.write_packet(pck.data, pck.stream_serial(), inf, pck.absgp_page());
    }
});
```

```bash
mkdir fuzz/corpus/fuzz_target_1/
curl -o fuzz/corpus/fuzz_target_1/sample.ogg https://commons.wikimedia.org/wiki/File:320x240.ogg
cargo +nightly fuzz run fuzz_target_1
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "requires nightly" | Use `cargo +nightly fuzz` |
| Slow performance | Add `--sanitizer none` for safe Rust |
| "cannot find binary" | Move code from `main.rs` to `lib.rs` |
| Sanitizer compilation issues | Try different nightly: `rustup install nightly-2024-01-01` |
| Low coverage | Add seeds to `fuzz/corpus/fuzz_target_1/`, use dictionary |

## Resources

- [Rust Fuzz Book](https://rust-fuzz.github.io/book/cargo-fuzz.html)
- [arbitrary crate](https://docs.rs/arbitrary/latest/arbitrary/)
- [cargo-fuzz GitHub](https://github.com/rust-fuzz/cargo-fuzz)
