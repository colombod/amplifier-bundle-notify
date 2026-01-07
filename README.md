# amplifier-bundle-notify

Desktop notifications when Amplifier assistant turns complete.

## Overview

This bundle provides native desktop notifications that fire when the assistant finishes processing and is ready for user input. Perfect for long-running operations where you might switch to another window.

## Features

- **Cross-platform support**: macOS, Linux, Windows, and WSL
- **Configurable thresholds**: Only notify on multi-iteration turns
- **Sound support**: Optional notification sounds (macOS)
- **Expert agent**: Consultation for configuration and troubleshooting

## Installation

### From Source

```bash
# Install the hooks module
cd modules/hooks-notify
pip install -e .

# Install the bundle
cd ../..
pip install -e .
```

### Platform Requirements

**Linux:**
```bash
sudo apt install libnotify-bin  # Ubuntu/Debian
```

**macOS/Windows:** No additional requirements.

## Usage

### Include in Your Bundle

```yaml
# your-bundle.yaml
includes:
  - notify
```

### Or Use the Behavior

```yaml
# your-bundle.yaml
behaviors:
  - notify:desktop-notifications
```

### Configuration

```yaml
# settings.yaml or bundle config
hooks:
  notify:
    enabled: true           # Enable/disable notifications
    title: "Amplifier"      # Notification title
    min_iterations: 2       # Only notify for multi-iteration turns
    show_iteration_count: true
    sound: false            # macOS only
```

## Components

| Component | Description |
|-----------|-------------|
| `hooks-notify` | Hook module that sends notifications |
| `notify-expert` | Agent for configuration help |
| `desktop-notifications` | Ready-to-use behavior |

## Events

This bundle hooks into:

| Event | When |
|-------|------|
| `orchestrator:complete` | Assistant turn finished |

## Extending

See `context/NOTIFICATIONS.md` for:
- Adding webhook support for mobile push
- Integrating with Slack/Teams
- Adding custom notification providers

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
