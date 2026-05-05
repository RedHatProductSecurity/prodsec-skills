---
name: compiler-hardening
description: >
  Apply compiler hardening flags and sanitizers to C/C++ builds. Use when
  reviewing build configurations, CI pipelines, or Makefiles/CMakeLists for
  native code projects.
category: "secure_development"
subcategory: "languages"
---

# Compiler Hardening

## Common Vulnerability Classes

| Category | Examples |
|---|---|
| **Memory errors** | Buffer overflow, use-after-free (UAF), buffer over-read |
| **Dependency attacks** | Library hijacking, library sideloading, supply chain compromise |

## Hardening Flags

When building with Fedora/RPM toolchains, hardened flags are often applied automatically. For other build systems, explicitly add hardening options.

The [OpenSSF Compiler Hardening Guide](https://github.com/ossf/wg-best-practices-os-developers/blob/main/docs/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C%2B%2B.md) is the canonical reference. Key flags include:

| Flag | Purpose |
|---|---|
| `-fstack-protector-strong` | Stack buffer overflow detection |
| `-D_FORTIFY_SOURCE=2` | Runtime buffer overflow checks for standard library functions |
| `-fPIE` / `-pie` | Position-independent executable for ASLR |
| `-Wl,-z,relro,-z,now` | Full RELRO -- makes GOT read-only after relocation |
| `-Wl,-z,noexecstack` | Non-executable stack |
| `-fno-strict-overflow` | Prevent undefined behavior optimizations on signed overflow |

GCC 14+ provides `-fhardened` as a convenience flag that enables a recommended set of hardening options.

The [Fedora Security Features Matrix](https://fedoraproject.org/wiki/Security_Features_Matrix) provides an overview of security features available in a modern Linux system.

## Sanitizers

Sanitizers add runtime instrumentation that catches errors during testing that would otherwise go undetected. They increase binary size and resource consumption but provide significantly better error detection and debug information than traditional tooling.

| Sanitizer | Flag | Detects |
|---|---|---|
| [AddressSanitizer](https://github.com/google/sanitizers/wiki/AddressSanitizer) | `-fsanitize=address` | Memory access violations (buffer overflow, UAF, stack overflow) |
| [ThreadSanitizer](https://github.com/google/sanitizers/wiki#threadsanitizer) | `-fsanitize=thread` | Data races and race conditions |
| [LeakSanitizer](https://github.com/google/sanitizers/wiki/AddressSanitizerLeakSanitizer) | `-fsanitize=leak` | Memory leaks |
| [UndefinedBehaviorSanitizer](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html) | `-fsanitize=undefined` | Undefined behavior at runtime |

Run sanitizer-enabled builds in CI. ASan and UBSan are the highest-value sanitizers for most projects.

## Security Considerations

### W^X and JIT Compilers

JIT compilers inherently conflict with W^X (write XOR execute) because they must generate executable code at runtime. W^X protections apply at page granularity and cannot be meaningfully enforced on JIT buffers. Other memory areas (thread stacks, heap) should still have NX (non-executable) protection.

### Sandboxing

User-space sandboxing alone is **insufficient**; prefer OS and process-level isolation (namespaces, seccomp, SELinux) as the primary security boundary. User-space sandboxes can serve as defense-in-depth but have historically introduced their own security bugs and should not be the sole barrier, especially post-Spectre.

### Dynamic Linking

Dynamic linking relies on well-known search paths and filesystem permissions. The compilation environment may differ from the runtime environment with different (but compatible) library versions. Be aware of:

- Library search path attacks (`LD_LIBRARY_PATH`, `RPATH` manipulation)
- Symbol interposition risks
- Version mismatches between build and runtime

## Implementation Checklist

- [ ] Hardening flags are applied in the build system (or `-fhardened` with GCC 14+)
- [ ] `-fstack-protector-strong` is enabled
- [ ] `_FORTIFY_SOURCE=2` is defined
- [ ] PIE is enabled (`-fPIE -pie`)
- [ ] Full RELRO is enabled (`-Wl,-z,relro,-z,now`)
- [ ] At least ASan and UBSan run in CI
- [ ] Sanitizer failures block the CI pipeline
- [ ] JIT compiler memory regions are isolated from general-purpose allocations
- [ ] User-space sandboxing is not the sole security boundary; OS-level isolation is the primary layer
- [ ] Library search paths are reviewed for safety

## References

- [OpenSSF Compiler Hardening Guide](https://github.com/ossf/wg-best-practices-os-developers/blob/main/docs/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C%2B%2B.md)
- [Fedora Security Features Matrix](https://fedoraproject.org/wiki/Security_Features_Matrix)
- [Google Sanitizers wiki](https://github.com/google/sanitizers/wiki)
