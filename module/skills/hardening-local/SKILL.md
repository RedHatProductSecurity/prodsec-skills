---
name: hardening-local
description: Harden locally deployed MCP servers against network exposure and host compromise. Use when building, deploying, or reviewing MCP servers that run on a user's local machine.
category: "secure_development"
subcategory: "mcp-server"
---

# Hardening Local MCP Servers

## Security Requirements

MCP servers running locally on a user's machine require specific hardening to prevent network exposure and protect the host.

## Network Binding

Bind to the loopback interface only:

```
# CORRECT - bind to loopback only
host: 127.0.0.1
port: 8080

# WRONG - exposed to the entire network
host: 0.0.0.0
port: 8080
```

Binding to `0.0.0.0` exposes the MCP server to the local network and potentially the internet, allowing unauthorized access.

## Process Isolation

| Control | Details |
|---|---|
| **Dedicated user** | Run as a dedicated low-privilege OS user, not the user's main account |
| **No root** | Never run as root |
| **Minimal permissions** | Grant only the filesystem and network permissions needed |
| **Filesystem isolation** | Use containers or chroot to limit host filesystem access |

## Host Protection

| Control | Details |
|---|---|
| **Containers** | Run in a container (Podman, Docker) to isolate from the host |
| **chroot** | Use chroot jail to limit filesystem visibility |
| **Read-only access** | Mount host directories as read-only when possible |
| **No home directory access** | Do not grant access to the user's entire home directory |

## Implementation Checklist

- [ ] Bind to `127.0.0.1` only, never `0.0.0.0`
- [ ] Run as a dedicated low-privilege OS user
- [ ] Never run as root
- [ ] Use filesystem isolation (container or chroot)
- [ ] Mount host directories as read-only where possible
- [ ] Limit accessible directories to only what the MCP server needs (respect roots)
- [ ] Verify no network interfaces other than loopback are exposed
