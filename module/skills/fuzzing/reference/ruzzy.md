---
name: ruzzy
description: >
  Coverage-guided Ruby fuzzer for pure Ruby code and C extensions.
---

# Ruzzy

Coverage-guided Ruby fuzzer by Trail of Bits, built on libFuzzer. Currently the only production-ready coverage-guided fuzzer for Ruby. Supports pure Ruby code and Ruby C extensions with ASan/UBSan.

## Installation

Supports Linux x86-64 and AArch64. For macOS/Windows, use the [Dockerfile](https://github.com/trailofbits/ruzzy/blob/main/Dockerfile).

```bash
MAKE="make --environment-overrides V=1" \
CC="/path/to/clang" CXX="/path/to/clang++" \
LDSHARED="/path/to/clang -shared" LDSHAREDXX="/path/to/clang++ -shared" \
    gem install ruzzy
```

Requires clang 14.0.0+. Debug with `RUZZY_DEBUG=1 gem install --verbose ruzzy`.

### Verify

```bash
export ASAN_OPTIONS="allocator_may_return_null=1:detect_leaks=0:use_sigaltstack=0"
LD_PRELOAD=$(ruby -e 'require "ruzzy"; print Ruzzy::ASAN_PATH') \
    ruby -e 'require "ruzzy"; Ruzzy.dummy'
```

Should quickly find a crash, confirming Ruzzy works.

## Fuzzing Pure Ruby

Pure Ruby requires two scripts (tracer + harness) due to interpreter implementation details.

**Tracer (`test_tracer.rb`):**

```ruby
require 'ruzzy'
Ruzzy.trace('test_harness.rb')
```

**Harness (`test_harness.rb`):**

```ruby
require 'ruzzy'
require_relative 'my_parser'

test_one_input = lambda do |data|
  begin
    MyParser.parse(data)
  rescue StandardError
  end
  return 0
end

Ruzzy.fuzz(test_one_input)
```

Run:

```bash
LD_PRELOAD=$(ruby -e 'require "ruzzy"; print Ruzzy::ASAN_PATH') ruby test_tracer.rb
```

## Fuzzing C Extensions

Single harness file, no tracer needed. Install the gem with sanitizer flags first:

```bash
MAKE="make --environment-overrides V=1" \
CC="/path/to/clang" CXX="/path/to/clang++" \
LDSHARED="/path/to/clang -shared" LDSHAREDXX="/path/to/clang++ -shared" \
CFLAGS="-fsanitize=address,fuzzer-no-link -fno-omit-frame-pointer -fno-common -fPIC -g" \
CXXFLAGS="-fsanitize=address,fuzzer-no-link -fno-omit-frame-pointer -fno-common -fPIC -g" \
    gem install your_gem
```

**Harness:**

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

Run:

```bash
LD_PRELOAD=$(ruby -e 'require "ruzzy"; print Ruzzy::ASAN_PATH') ruby harness.rb corpus/
```

## Running

```bash
export ASAN_OPTIONS="allocator_may_return_null=1:detect_leaks=0:use_sigaltstack=0"

# Basic
LD_PRELOAD=$(ruby -e 'require "ruzzy"; print Ruzzy::ASAN_PATH') ruby harness.rb

# With corpus and options
LD_PRELOAD=$(ruby -e 'require "ruzzy"; print Ruzzy::ASAN_PATH') \
    ruby harness.rb /path/to/corpus -max_len=1024 -timeout=10

# Reproduce crash
LD_PRELOAD=$(ruby -e 'require "ruzzy"; print Ruzzy::ASAN_PATH') \
    ruby harness.rb ./crash-<hash>
```

**Important:** Set `LD_PRELOAD` inline, don't export it — it interferes with other programs.

All [libFuzzer options](https://llvm.org/docs/LibFuzzer.html#options) work as arguments.

### UBSan

```bash
LD_PRELOAD=$(ruby -e 'require "ruzzy"; print Ruzzy::UBSAN_PATH') ruby harness.rb
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Installation fails | Verify clang path, use clang 14.0.0+ |
| `cannot open shared object file` | Set `LD_PRELOAD` inline with ruby command |
| No coverage progress (pure Ruby) | Use tracer script |
| Leak detection spam | `ASAN_OPTIONS=detect_leaks=0` |

## Resources

- [Ruzzy GitHub](https://github.com/trailofbits/ruzzy)
- [Introducing Ruzzy](https://blog.trailofbits.com/2024/03/29/introducing-ruzzy-a-coverage-guided-ruby-fuzzer/)
- [libFuzzer Options](https://llvm.org/docs/LibFuzzer.html)
