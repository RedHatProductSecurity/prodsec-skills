---
name: os-tool-security
description: Enforce least privilege and sandboxing for MCP server OS tool execution. Use when building, configuring, or reviewing MCP servers that execute operating system commands or local tools.
category: "secure_development"
subcategory: "mcp-server"
---

# OS Tool Security for MCP Servers

## Security Requirement

When MCP servers execute tools in the operating system, they run with the permissions of the MCP server process. The following security controls are required:

1. **Least Privilege**: Give the MCP server the lowest permissions necessary to perform its mission.
2. **Privilege Dropping**: Drop specific privileges before executing specific commands.
3. **Sandboxing**: Use sandboxing mechanisms to prevent executed commands from causing damage.

## Command Execution Hygiene

Never pass unsanitized input to a shell. Use safe, parameterized APIs:

```python
import subprocess

# CORRECT - parameterized, no shell
subprocess.run(['echo', user_input], shell=False)

# FORBIDDEN - shell injection risk
import os
os.system(f"echo {user_input}")          # NEVER do this
subprocess.run(f"echo {user_input}", shell=True)  # NEVER do this
```

Never execute commands with higher privileges than necessary. Never run as root.

## Least Privilege

- Run the MCP server process under a dedicated, unprivileged user account
- Grant only the specific filesystem, network, and system permissions required
- Use capability-based security (Linux capabilities) instead of running as root
- Separate read-only and read-write filesystem access

## Privilege Dropping

Before executing a command, drop privileges not required for that specific command:

```python
# Drop to restricted user before executing tool command
import os

def execute_tool_command(command, restricted_uid, restricted_gid):
    pid = os.fork()
    if pid == 0:
        os.setgid(restricted_gid)
        os.setuid(restricted_uid)
        os.execvp(command[0], command)
    else:
        _, status = os.waitpid(pid, 0)
        return status
```

## Sandboxing Mechanisms

Use one or more of the following to contain tool execution:

| Mechanism | Description |
|---|---|
| **Containers** (Podman, Docker) | Isolate tool execution in a container with limited capabilities |
| **seccomp** | Restrict system calls available to the tool process |
| **AppArmor / SELinux** | Mandatory access control policies limiting file and network access |
| **namespaces** | Isolate PID, network, mount, and user namespaces |
| **chroot / pivot_root** | Restrict filesystem visibility |
| **cgroups** | Limit CPU, memory, and I/O resources |

## Implementation Checklist

- [ ] Never use `os.system()` or `shell=True`; use parameterized APIs (`subprocess.run` with `shell=False`)
- [ ] Never execute commands as root
- [ ] Run MCP server under a dedicated, unprivileged service account
- [ ] Audit all OS commands the MCP server needs to execute
- [ ] Grant only the minimum filesystem and network permissions required
- [ ] Implement privilege dropping before executing each tool command
- [ ] Deploy sandboxing (containers, seccomp, AppArmor/SELinux, or namespaces)
- [ ] Set resource limits (cgroups) on tool execution processes
- [ ] Log all OS tool executions including the command, user context, and exit status
- [ ] Deny-list dangerous commands and system calls by default
