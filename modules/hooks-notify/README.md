# hooks-notify

Desktop notifications when the assistant completes a turn and is ready for user input.

## Overview

This hook module listens for `orchestrator:complete` events and sends native desktop notifications to alert the user that Amplifier is ready for their next input. This is especially useful for long-running operations where you might switch to another window.

## Platform Support

| Platform | Method | Notes |
|----------|--------|-------|
| macOS | osascript | Native Notification Center |
| Linux | notify-send | Requires `libnotify-bin` package |
| WSL | PowerShell | Windows toast notifications |
| Windows | PowerShell | Windows toast notifications |

## Installation

### Linux (Ubuntu/Debian)
```bash
sudo apt install libnotify-bin
```

### macOS
No additional installation required.

### Windows/WSL
No additional installation required (uses built-in PowerShell).

## Configuration

```yaml
# In your bundle or settings.yaml
hooks:
  notify:
    enabled: true           # Enable/disable notifications
    title: "Amplifier"      # Notification title
    min_iterations: 1       # Minimum loop iterations to trigger
    show_iteration_count: true  # Show iteration count in message
    sound: false            # Play sound (macOS only)
    debug: false            # Enable debug logging
```

## Events

This hook subscribes to:

| Event | Description |
|-------|-------------|
| `orchestrator:complete` | Fires when the orchestrator loop finishes |

## Example Notification

When the assistant completes a multi-iteration turn:

```
Title: Amplifier
Subtitle: loop-streaming
Message: Ready (3 iterations)
```

## Extending

To add support for additional events or notification types, you can:

1. Fork this module
2. Add handlers for other events (e.g., `tool:error`, `session:end`)
3. Implement webhook support for mobile push notifications

## License

MIT
