# amplifier-bundle-notify

Desktop and push notifications when Amplifier assistant turns complete.

## Overview

This bundle provides notification hooks that fire when the assistant finishes processing and is ready for user input. Perfect for long-running operations where you might switch to another window or connect remotely.

**This is a Policy Behavior** - notifications only fire for root/interactive sessions, not for sub-agents, recipe steps, or other child sessions. See [Policy Behaviors](https://github.com/microsoft/amplifier-foundation/blob/main/docs/POLICY_BEHAVIORS.md) for details.

## Features

- **Cross-platform desktop**: macOS, Linux, Windows, and WSL
- **Terminal notifications**: OSC escape sequences that work over SSH
- **Push notifications**: ntfy.sh integration for mobile alerts
- **Multi-method support**: Enable desktop AND push simultaneously
- **Root-session only**: Automatically skips sub-agents and recipe steps
- **Focus detection**: Optionally suppress when terminal is focused
- **Configurable thresholds**: Only notify on multi-iteration turns

## Recommended Usage: App-Level Configuration

The recommended way to use notifications is via `settings.yaml`, letting the app compose the hooks at runtime:

```yaml
# ~/.amplifier/settings.yaml
config:
  notifications:
    desktop:
      enabled: true
      title: "Amplifier"
      subtitle: "cwd"           # "cwd", "git", or custom string
      suppress_if_focused: true
      sound: false              # macOS only
    
    push:
      enabled: true
      service: ntfy
      topic: "my-amplifier-alerts"  # Your secret topic
      server: "https://ntfy.sh"
      priority: default
    
    # Common options
    min_iterations: 1
    show_iteration_count: true
```

This approach:
- Only fires for root sessions (not sub-agents)
- Works with any bundle (foundation, recipes, custom)
- Allows multiple notification methods simultaneously

## Alternative: Direct Bundle Inclusion

You can also include notifications directly in a bundle (not recommended for most cases):

```yaml
# your-bundle.yaml
includes:
  - bundle: git+https://github.com/microsoft/amplifier-bundle-notify@main
```

**Warning**: Direct inclusion fires for ALL sessions including sub-agents. Use the `settings.yaml` approach above for policy-aware notifications.

## Components

| Component | Description |
|-----------|-------------|
| `hooks-notify` | Desktop/terminal notifications |
| `hooks-notify-push` | Push notifications via ntfy.sh |
| `notify-expert` | Agent for configuration help |

## Configuration Options

### Desktop Notifications (`hooks-notify`)

| Option | Default | Description |
|--------|---------|-------------|
| `enabled` | `true` | Enable/disable notifications |
| `method` | `"auto"` | `"auto"`, `"terminal"`, or `"desktop"` |
| `title` | `"Amplifier"` | Notification title |
| `subtitle` | `"cwd"` | `"cwd"`, `"git"`, or custom string |
| `suppress_if_focused` | `true` | Skip if terminal appears focused |
| `min_iterations` | `1` | Only notify after N iterations |
| `show_iteration_count` | `true` | Show iteration count in message |
| `sound` | `false` | Play sound (macOS desktop only) |

### Push Notifications (`hooks-notify-push`)

| Option | Default | Description |
|--------|---------|-------------|
| `enabled` | `false` | Enable/disable (requires `NTFY_TOPIC` env var if not configured) |
| `service` | `"ntfy"` | Push service (currently only ntfy supported) |
| `topic` | - | Your ntfy topic (treat like a password) |
| `server` | `"https://ntfy.sh"` | ntfy server URL |
| `priority` | `"default"` | `min`, `low`, `default`, `high`, `urgent` |

## Disabling Notifications

**Option 1: Environment Variable** (per-session)

```bash
AMPLIFIER_NOTIFY=false amplifier run "..."
```

**Option 2: Settings** (persistent)

```yaml
# ~/.amplifier/settings.yaml
config:
  notifications: {}  # Empty = disabled
```

## Events

### Listens To

| Event | When |
|-------|------|
| `orchestrator:complete` | Assistant turn finished |

### Emits

| Event | Data | Description |
|-------|------|-------------|
| `notify:turn-complete` | `{session_id, turn_count, status, project, message}` | Normalized turn completion for downstream hooks |

## Platform Requirements

**Linux:**
```bash
sudo apt install libnotify-bin  # Ubuntu/Debian
```

**macOS/Windows:** No additional requirements.

**Push notifications:** Install the [ntfy app](https://ntfy.sh/) and subscribe to your topic.

## Extending

The `notify:turn-complete` event allows you to build additional notification handlers:

```python
@coordinator.hooks.register("notify:turn-complete")
async def my_custom_notifier(event: str, data: dict) -> HookResult:
    # Send to Slack, Teams, Discord, etc.
    await send_to_slack(data["message"], data["project"])
    return HookResult(action="continue")
```

## Contributing

> [!NOTE]
> This project is not currently accepting external contributions, but we're actively working toward opening this up. We value community input and look forward to collaborating in the future. For now, feel free to fork and experiment!

Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit [Contributor License Agreements](https://cla.opensource.microsoft.com).

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
