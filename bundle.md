---
bundle:
  name: notify
  version: 0.1.0
  description: Desktop and terminal notifications when assistant turns complete

# Include the desktop notifications behavior by default
includes:
  - bundle: notify:behaviors/desktop-notifications
---

# Notify Bundle

This bundle provides desktop and terminal notifications when the assistant completes a turn and is ready for user input.

## Features

- **Cross-platform support**: macOS, Linux, Windows/WSL
- **SSH-aware**: Uses terminal bell sequences over SSH, desktop notifications locally
- **Focus detection**: Optionally suppress notifications when terminal is focused
- **Extensible**: Emits `notify:turn-complete` event for custom notification handlers

## Quick Start

Include in your bundle:

```yaml
includes:
  - bundle: git+https://github.com/microsoft/amplifier-bundle-notify@main
```

Or include just the behavior:

```yaml
includes:
  - bundle: git+https://github.com/microsoft/amplifier-bundle-notify@main#subdirectory=behaviors/desktop-notifications.yaml
```

## Configuration

The default behavior can be customized via the `hooks-notify` config:

```yaml
hooks:
  - module: hooks-notify
    source: git+https://github.com/microsoft/amplifier-bundle-notify@main#subdirectory=modules/hooks-notify
    config:
      enabled: true
      method: auto          # "auto", "terminal", or "desktop"
      title: "Amplifier"
      subtitle: "cwd"       # "cwd", "git", or custom string
      suppress_if_focused: true
      min_iterations: 1
      show_iteration_count: true
      sound: false
```

## Extending

See [docs/EXTENDING.md](docs/EXTENDING.md) for guidance on creating custom notification handlers (Slack, Teams, webhooks, etc.).

## Events

This bundle emits the `notify:turn-complete` event after sending notifications:

```python
{
    "session_id": "...",
    "turn_count": 3,
    "status": "success",
    "project": "my-project",
    "message": "Ready (3 iterations)",
    "notification_sent": True,
}
```

Custom hooks can listen to this event instead of parsing `orchestrator:complete` directly.
