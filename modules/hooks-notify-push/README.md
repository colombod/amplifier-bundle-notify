# hooks-notify-push

Push notifications via ntfy.sh when the Amplifier assistant completes a turn.

Perfect for mobile devices (Termius, JuiceSSH) where terminal escape sequences don't trigger system notifications.

## Quick Start

1. **Pick a secret topic name** (treat it like a password):
   ```bash
   export AMPLIFIER_NTFY_TOPIC="my-amplifier-abc123"
   ```

2. **Subscribe on your phone**:
   - Install [ntfy app](https://ntfy.sh/) (Android/iOS)
   - Subscribe to your topic

3. **Run Amplifier** - you'll get push notifications when ready for input!

## Configuration

### Environment Variables (Recommended)

```bash
# Required: Your ntfy.sh topic
export AMPLIFIER_NTFY_TOPIC="your-secret-topic"

# Optional: Use self-hosted server
export AMPLIFIER_NTFY_SERVER="https://ntfy.your-domain.com"

# Optional: Disable push notifications
export AMPLIFIER_PUSH_ENABLED=false
```

### Bundle Configuration

```yaml
hooks:
  - module: hooks-notify-push
    source: git+https://github.com/microsoft/amplifier-bundle-notify@main#subdirectory=modules/hooks-notify-push
    config:
      topic: "your-secret-topic"  # or use AMPLIFIER_NTFY_TOPIC
      server: "https://ntfy.sh"   # default
      priority: "default"         # min, low, default, high, urgent
      tags: ["robot"]             # emoji tags
      listen_event: "notify:turn-complete"  # or "orchestrator:complete"
```

## How It Works

By default, this hook listens to `notify:turn-complete` events emitted by `hooks-notify`. This gives it access to:
- Pre-computed project name
- Human-readable message
- Notification status

Alternatively, set `listen_event: "orchestrator:complete"` for independent operation without requiring `hooks-notify`.

## Security Notes

- **Topics are public by default** on ntfy.sh - treat your topic name like a password
- Use a random topic name (e.g., `amplifier-x7k9m2p4`)
- For private notifications, consider [self-hosting ntfy](https://docs.ntfy.sh/install/)
- Or use [ntfy.sh access control](https://docs.ntfy.sh/publish/#access-tokens)

## Supported Services

Currently supports:
- **ntfy.sh** - Free, open-source, no signup required

Future support planned for:
- Pushover
- Pushbullet
- Custom webhooks
