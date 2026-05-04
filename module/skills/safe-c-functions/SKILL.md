---
name: safe-c-functions
description: >
  Apply when reviewing or writing C/C++ code that uses memory or
  string operations. Identifies banned functions, provides safe
  replacements, compiler hardening flags, and refactoring examples.
license: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)
origin: Adapted from CoSAI Project CodeGuard (https://github.com/cosai-oasis/project-codeguard)
category: "secure_development"
subcategory: "languages"
---

# C/C++ Memory and String Safety

Actively identify, flag, and provide secure refactoring options for insecure memory and string functions. When generating new code, always default to the safest function available.

## Insecure Functions and Safe Alternatives

### Critical / High Risk

**`gets()`** -- Critical. No bounds checking whatsoever. Always replace with:
- `fgets(char *str, int n, FILE *stream)`

**`strcpy()`** -- High risk. Copies until null terminator with no bounds check. Replace with:
- `snprintf()`, `strcpy_s()` (C11 Annex K), or `strncpy()` (with manual null termination)

**`strcat()`** -- High risk. Appends with no bounds check. Replace with:
- `snprintf()`, `strcat_s()` (C11 Annex K), or `strncat()` (with careful handling)

**`sprintf()` / `vsprintf()`** -- High risk. No output buffer bounds check. Replace with:
- `snprintf()`, `vsprintf_s()` (C11 Annex K)

### Medium Risk

**`scanf()` family** -- `%s` without width limit causes buffer overflows.
1. Use width specifiers: `scanf("%127s", buffer)`
2. Better: read with `fgets()` then parse with `sscanf()`

**`strtok()`** -- Not reentrant or thread-safe (static internal buffer). Replace with:
- `strtok_r()` (POSIX) or `strtok_s()` (C11 Annex K)

**`memcpy()` / `memmove()`** -- Not inherently insecure but common source of bugs with miscalculated sizes. Prefer `memcpy_s()` / `memmove_s()` when available.

## Banned Memory Functions

| Banned | Safe Replacement |
|--------|-----------------|
| `memcpy()` | `memcpy_s()` |
| `memset()` | `memset_s()` |
| `memmove()` | `memmove_s()` |
| `memcmp()` | `memcmp_s()` |
| `bzero()` | `memset_s()` |
| `memzero()` | `memset_s()` |

## Banned String Functions

| Banned | Safe Replacement |
|--------|-----------------|
| `strstr()` | `strstr_s()` |
| `strtok()` | `strtok_s()` |
| `strcpy()` | `strcpy_s()` |
| `strcmp()` | `strcmp_s()` |
| `strlen()` | `strnlen_s()` |
| `strcat()` | `strcat_s()` |
| `sprintf()` | `snprintf()` |

## New Code Guidelines

- NEVER generate code using `gets()`, `strcpy()`, `strcat()`, or `sprintf()`.
- DEFAULT to `snprintf()` for string formatting and concatenation.
- DEFAULT to `fgets()` for reading string input from files or stdin.

## Compiler Hardening Flags

- **Stack protection**: `-fstack-protector-all` or `-fstack-protector-strong`
- **Address sanitizer**: `-fsanitize=address` (development builds)
- **Object size checking**: `-D_FORTIFY_SOURCE=2` (runtime bounds checks for unsafe functions)
- **Format string protection**: `-Wformat -Wformat-security`

## Refactoring Examples

### Replacing `strcpy`

```c
// UNSAFE
char destination[64];
strcpy(destination, source_string);

// SAFE
char destination[64];
snprintf(destination, sizeof(destination), "%s", source_string);
```

### Correcting `strncpy` Usage

```c
// UNSAFE -- may not null-terminate if strlen(source) >= 10
char dest[10];
strncpy(dest, source, sizeof(dest));

// SAFE -- explicit null termination
char dest[10];
strncpy(dest, source, sizeof(dest) - 1);
dest[sizeof(dest) - 1] = '\0';
```

### Securing `scanf`

```c
// UNSAFE
char user_name[32];
scanf("%s", user_name);

// SAFE
char user_name[32];
if (fgets(user_name, sizeof(user_name), stdin)) {
    user_name[strcspn(user_name, "\n")] = 0;
}
```

### Safe String Copy Pattern

```c
// UNSAFE
char dest[256];
strcpy(dest, src);

// SAFE
char dest[256];
errno_t result = strcpy_s(dest, sizeof(dest), src);
if (result != 0) {
    // Handle error: src too long or invalid parameters
    return ERROR;
}
```

### Safe String Concatenation Pattern

```c
// UNSAFE
char buffer[256] = "prefix_";
strcat(buffer, suffix);

// SAFE
char buffer[256] = "prefix_";
errno_t result = strcat_s(buffer, sizeof(buffer), suffix);
if (result != 0) {
    return ERROR;
}
```

### Safe Memory Copy Pattern

```c
// UNSAFE
memcpy(dest, src, size);

// SAFE
errno_t result = memcpy_s(dest, dest_max_size, src, size);
if (result != 0) {
    return ERROR;
}
```

### Safe String Tokenization Pattern

```c
// UNSAFE
char *token = strtok(str, delim);

// SAFE
char *next_token = NULL;
rsize_t str_max = strnlen_s(str, MAX_STRING_SIZE);
char *token = strtok_s(str, &str_max, delim, &next_token);
while (token != NULL) {
    // Process token
    token = strtok_s(NULL, &str_max, delim, &next_token);
}
```

## Common Pitfalls

### Pitfall 1: Wrong Size Parameter

```c
// WRONG -- using source size instead of destination size
strcpy_s(dest, strlen(src), src);

// CORRECT -- using destination buffer size
strcpy_s(dest, sizeof(dest), src);
```

### Pitfall 2: Ignoring Return Values

```c
// WRONG -- error not checked
strcpy_s(dest, sizeof(dest), src);

// CORRECT -- checking return value
if (strcpy_s(dest, sizeof(dest), src) != 0) {
    // Handle error
}
```

### Pitfall 3: Using sizeof() on Pointers

```c
// WRONG -- sizeof(char*) = 8, not the buffer size
void func(char *buffer) {
    strcpy_s(buffer, sizeof(buffer), src);
}

// CORRECT -- pass buffer size as parameter
void func(char *buffer, size_t buffer_size) {
    strcpy_s(buffer, buffer_size, src);
}
```

## Code Review Checklist

### Developer Pre-Review

- [ ] No unsafe memory functions (`memcpy`, `memset`, `memmove`, `memcmp`, `bzero`)
- [ ] No unsafe string functions (`strcpy`, `strcat`, `strcmp`, `strlen`, `sprintf`, `strstr`, `strtok`)
- [ ] All memory operations use `*_s()` variants with proper size parameters
- [ ] Buffer sizes correctly calculated using `sizeof()` or known limits
- [ ] No hardcoded buffer sizes that could change

### Reviewer Checks

- [ ] All memory operations use safe variants
- [ ] Destination buffer sizes properly specified
- [ ] All `errno_t` return values handled
- [ ] `rsize_t dmax` parameters are correct
- [ ] Strings properly null-terminated
- [ ] Source string lengths validated before operations

### Static Analysis Integration

- [ ] Compiler warnings enabled for unsafe function usage
- [ ] Static analysis tools configured to detect unsafe function calls
- [ ] Build system treats unsafe function warnings as errors
- [ ] Pre-commit hooks scan for banned functions
