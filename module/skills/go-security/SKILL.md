---
name: go-security
description: >
  Enforce secure coding practices in Go applications. Use when building,
  reviewing, or auditing Go code that handles user input, database access,
  cryptography, TLS, or uses unsafe/cgo.
category: "secure_development"
subcategory: "languages"
---

# Go Security

## Dependency Management

- Use **Go modules** for all dependency management
- The `go.sum` checksum database provides assurance against module mutation
- Pin dependency versions, including transitive modules
- Run `govulncheck` regularly to scan for known vulnerabilities in dependencies

## Input Validation

- Validate all user input using Go native packages (`strconv`, `regexp`) or third-party validators like [go-playground/validator](https://github.com/go-playground/validator)
- Never trust input from external sources without validation

## XSS Prevention

Use `html/template` (not `text/template`) for rendering HTML. It applies contextual autoescaping for HTML, CSS, JavaScript, and URL contexts.

```go
name := r.FormValue("name")
tmpl := template.Must(template.ParseGlob("page.html"))
data["Name"] = name
err := tmpl.ExecuteTemplate(w, "page", data)
```

Use [nosurf](https://github.com/justinas/nosurf) for CSRF prevention in HTTP handlers.

## SQL Injection Prevention

Use **parameterized queries**. In Go, statements are prepared on the DB, not the connection:

```go
customerName := r.URL.Query().Get("name")
db.Exec("UPDATE creditcards SET name=? WHERE customerId=?", customerName, 233)
```

When using `db.Query()` with string formatting, sanitize all input first.

## Cryptography

- Use Go's standard `crypto` and `golang.org/x/crypto` packages
- Do not implement custom cryptographic algorithms
- Use well-established algorithms (AES-GCM, ChaCha20-Poly1305, Ed25519)

## HTTPS and TLS

Enforce HTTPS with HSTS headers and explicit TLS server configuration:

```go
w.Header().Add("Strict-Transport-Security", "max-age=63072000; includeSubDomains")
```

```go
config := &tls.Config{ServerName: "yourServiceName"}
```

Always encrypt in-transit communication, even for internal services.

## unsafe and cgo

### unsafe Package

- The `unsafe` package bypasses Go's type system; subtle mistakes are common
- Avoid `unsafe` unless there is no alternative (low-level system calls, performance-critical FFI)
- Verify safe usage with Go's vet tooling

### cgo

Avoid cgo when possible. Known issues:

- Breaks Go's cross-compilation
- Increases binary size and reduces portability
- cgo calls are significantly slower than native Go calls
- Puts Go's concurrency model at risk
- May break static binary linking

## Error Handling and Logging

- Handle every error explicitly (`if err != nil`)
- Never log secrets, tokens, API keys, or PII
- Sanitize data before including it in log output
- Do not expose internal error details in user-facing responses

## nil Pointer Safety

When unmarshalling JSON into structs with pointer fields, unset pointers remain `nil`. Dereferencing them causes a panic:

```go
type Foo struct {
    Bar *Bar
}

var f Foo
json.Unmarshal([]byte(`{"other":"data"}`), &f)
// f.Bar is nil -- accessing f.Bar.Field will panic
```

Always check pointer fields for nil before dereferencing.

## Tooling

| Tool | Purpose |
|---|---|
| [govulncheck](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck) | Scan dependencies for known vulnerabilities |
| [golangci-lint](https://golangci-lint.run/) | Aggregated linter collection |
| [gosec](https://github.com/securego/gosec) | Go security checker |

## Implementation Checklist

- [ ] Go modules are used with `go.sum` integrity checking
- [ ] `govulncheck` runs in CI
- [ ] All user input is validated before use
- [ ] `html/template` is used for HTML rendering (not `text/template`)
- [ ] SQL queries use parameterized statements
- [ ] Standard `crypto` packages are used (no custom crypto)
- [ ] HSTS is set and TLS is configured with explicit `ServerName`
- [ ] `unsafe` and `cgo` usage is justified, minimized, and reviewed
- [ ] Errors are handled explicitly; no secrets in logs or error responses
- [ ] Pointer fields are checked for nil before dereferencing

## References

- [Go Modules Reference](https://golang.org/ref/mod)
- [govulncheck](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck)
- [OWASP Go Secure Coding Practices](https://github.com/OWASP/Go-SCP)
- [Snyk: Go Security Cheatsheet](https://snyk.io/blog/go-security-cheatsheet-for-go-developers/)
