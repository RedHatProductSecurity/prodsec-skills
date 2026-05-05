---
name: react-security
description: >
  Enforce XSS prevention and secure rendering in React applications. Use when
  building, reviewing, or auditing React components, especially those that
  render user-controlled data or use server-side rendering.
category: "secure_development"
subcategory: "web-security"
---

# React Security

React escapes values rendered via JSX data binding by default, but several patterns can reintroduce XSS vulnerabilities. This skill covers the most common pitfalls.

## Default Data Binding

React automatically escapes values inside curly braces when rendering text content. This protection does **not** apply to HTML attributes.

**Safe -- text content is escaped:**

```jsx
<div>{userData}</div>
```

**Unsafe -- attribute values are not automatically escaped:**

```jsx
<form action={userData}>...</form>
```

Always validate or sanitize values placed in HTML attributes, especially `href`, `src`, `action`, and event handler attributes.

## dangerouslySetInnerHTML

Never pass unsanitized data to `dangerouslySetInnerHTML`. Always sanitize with a library like DOMPurify before rendering raw HTML.

**Safe:**

```jsx
import DOMPurify from "dompurify";
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(data) }} />
```

**Unsafe:**

```jsx
this.myRef.current.innerHTML = attackerControlledValue;
```

Direct DOM manipulation via refs bypasses React's escaping entirely.

## URL Validation

URLs can contain executable content via `javascript:` protocol URIs. Validate that URLs use `http:` or `https:` before rendering them.

**Safe:**

```jsx
function validateURL(url) {
  const parsed = new URL(url);
  return ["https:", "http:"].includes(parsed.protocol);
}

<a href={validateURL(url) ? url : ""}>Click here</a>
```

**Unsafe:**

```jsx
<a href={attackerControlled}>Click here</a>
```

## Server-Side Rendering (SSR)

`ReactDOMServer.renderToString()` and `ReactDOMServer.renderToStaticMarkup()` provide automatic content escaping for data bound through JSX. Do **not** concatenate unsanitized data with their output.

**Unsafe SSR pattern:**

```jsx
const html = ReactDOMServer.renderToString(<App />) + unsanitizedData;
```

## JSON Injection in Preloaded State

When embedding serialized state in SSR HTML, escape HTML-significant characters to prevent script injection via closing `</script>` tags.

**Safe:**

```jsx
window.__PRELOADED_STATE__ = ${JSON.stringify(preloadedState).replace(/</g, "\\u003c")}
```

## Implementation Checklist

- [ ] User data is rendered via JSX `{}` binding, not string concatenation
- [ ] `dangerouslySetInnerHTML` is only used with DOMPurify-sanitized content
- [ ] No direct DOM writes via `ref.current.innerHTML`
- [ ] All `href` and `src` values are validated for `http:`/`https:` protocol
- [ ] SSR output is not concatenated with unsanitized strings
- [ ] Preloaded JSON state escapes `<` as `\u003c`
- [ ] No user-controlled data flows into `eval()`, `Function()`, or inline event handlers

## References

- [React documentation](https://react.dev/)
- [Snyk: 10 React Security Best Practices](https://snyk.io/blog/10-react-security-best-practices/)
