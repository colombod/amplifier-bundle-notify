# Extending the Notify Bundle

This guide explains how to create custom notification handlers that integrate with the Amplifier notification ecosystem.

## Architecture Overview

The notify bundle follows Amplifier's "composition over configuration" philosophy. Rather than building a plugin system, extensibility comes from **parallel hooks** that each listen to the same events independently.

```
orchestrator:complete
         │
         ├──▶ hooks-notify (terminal/desktop)
         ├──▶ hooks-notify-slack (your Slack module)
         ├──▶ hooks-notify-teams (your Teams module)
         └──▶ hooks-notify-mobile (your push notification module)
```

Each notification destination is a **separate hook module** that:
1. Listens to events directly
2. Implements its own logic
3. Gets composed via bundle includes

## Events You Can Listen To

### Option 1: `orchestrator:complete` (Raw Event)

Listen directly to the orchestrator event. No dependency on the notify bundle.

```python
async def handle_orchestrator_complete(event: str, data: dict) -> HookResult:
    """
    Event data:
    - session_id: str - The session identifier
    - turn_count: int - Number of iterations in this turn
    - status: str - "success" or error status
    - orchestrator: str - Which orchestrator ran (e.g., "loop-streaming")
    - parent_id: str | None - Parent session if this is a sub-agent
    """
    # Your notification logic here
    return HookResult(action="continue")
```

### Option 2: `notify:turn-complete` (Semantic Event)

Listen to the semantic event emitted by `hooks-notify`. This provides normalized, notification-focused data.

```python
async def handle_notify_turn_complete(event: str, data: dict) -> HookResult:
    """
    Event data:
    - session_id: str - The session identifier
    - turn_count: int - Number of iterations
    - status: str - "success" or error status
    - project: str - Resolved project name (from cwd, git, or config)
    - message: str - Human-readable message (e.g., "Ready (3 iterations)")
    - notification_sent: bool - Whether hooks-notify sent its notification
    """
    # Your notification logic here
    return HookResult(action="continue")
```

**When to use which:**

| Use Case | Recommended Event |
|----------|-------------------|
| Independent notification system | `orchestrator:complete` |
| Augmenting the notify bundle | `notify:turn-complete` |
| Need raw orchestrator data | `orchestrator:complete` |
| Want pre-computed message/project | `notify:turn-complete` |

## Creating a Custom Notification Hook

### Step 1: Create the Module

```python
# amplifier_module_hooks_notify_slack/__init__.py

import aiohttp
from dataclasses import dataclass
from typing import Any

@dataclass
class HookResult:
    action: str = "continue"

@dataclass
class SlackConfig:
    webhook_url: str
    channel: str | None = None
    username: str = "Amplifier"
    icon_emoji: str = ":robot_face:"
    min_iterations: int = 1

class SlackNotifyHook:
    """Send Slack notifications when Amplifier turns complete."""
    
    def __init__(self, config: SlackConfig):
        self.config = config
    
    async def handle_turn_complete(
        self, event: str, data: dict[str, Any]
    ) -> HookResult:
        """Handle notify:turn-complete or orchestrator:complete."""
        
        turn_count = data.get("turn_count", 0)
        if turn_count < self.config.min_iterations:
            return HookResult(action="continue")
        
        # Build Slack message
        project = data.get("project", "Amplifier")
        message = data.get("message", "Ready for input")
        
        payload = {
            "username": self.config.username,
            "icon_emoji": self.config.icon_emoji,
            "text": f"*{project}*: {message}",
        }
        
        if self.config.channel:
            payload["channel"] = self.config.channel
        
        # Send to Slack
        async with aiohttp.ClientSession() as session:
            await session.post(self.config.webhook_url, json=payload)
        
        return HookResult(action="continue")


async def mount(coordinator, config: dict | None = None):
    """Mount the Slack notification hook."""
    config = config or {}
    
    webhook_url = config.get("webhook_url")
    if not webhook_url:
        raise ValueError("webhook_url is required for hooks-notify-slack")
    
    slack_config = SlackConfig(
        webhook_url=webhook_url,
        channel=config.get("channel"),
        username=config.get("username", "Amplifier"),
        icon_emoji=config.get("icon_emoji", ":robot_face:"),
        min_iterations=config.get("min_iterations", 1),
    )
    
    hook = SlackNotifyHook(slack_config)
    
    # Choose which event to listen to:
    # Option A: Listen to semantic event (requires hooks-notify to be loaded)
    coordinator.hooks.register(
        "notify:turn-complete",
        hook.handle_turn_complete,
        priority=100,
        name="hooks-notify-slack",
    )
    
    # Option B: Listen to raw event (independent of hooks-notify)
    # coordinator.hooks.register(
    #     "orchestrator:complete",
    #     hook.handle_turn_complete,
    #     priority=100,
    #     name="hooks-notify-slack",
    # )
    
    return {
        "name": "hooks-notify-slack",
        "channel": slack_config.channel,
    }
```

### Step 2: Create the Behavior

```yaml
# behaviors/slack.yaml
bundle:
  name: notify-slack-behavior
  version: 1.0.0
  description: Slack notifications when assistant turns complete

hooks:
  - module: hooks-notify-slack
    source: git+https://github.com/yourorg/amplifier-module-hooks-notify-slack@main
    config:
      webhook_url: ${SLACK_WEBHOOK_URL}
      channel: "#amplifier-notifications"
      min_iterations: 2
```

### Step 3: Use in a Bundle

```yaml
# User's bundle
includes:
  - foundation
  - bundle: git+https://github.com/microsoft/amplifier-bundle-notify@main
  - bundle: git+https://github.com/yourorg/amplifier-bundle-notify@main#subdirectory=behaviors/slack.yaml
```

## Example: Webhook Notification Hook

A generic webhook hook that POSTs to any URL:

```python
# amplifier_module_hooks_notify_webhook/__init__.py

import aiohttp
from dataclasses import dataclass
from typing import Any

@dataclass
class HookResult:
    action: str = "continue"

@dataclass  
class WebhookConfig:
    url: str
    method: str = "POST"
    headers: dict | None = None
    include_session_id: bool = True
    include_turn_count: bool = True

class WebhookNotifyHook:
    def __init__(self, config: WebhookConfig):
        self.config = config
    
    async def handle_turn_complete(
        self, event: str, data: dict[str, Any]
    ) -> HookResult:
        payload = {
            "event": "turn_complete",
            "project": data.get("project"),
            "message": data.get("message"),
            "status": data.get("status"),
        }
        
        if self.config.include_session_id:
            payload["session_id"] = data.get("session_id")
        if self.config.include_turn_count:
            payload["turn_count"] = data.get("turn_count")
        
        headers = self.config.headers or {"Content-Type": "application/json"}
        
        async with aiohttp.ClientSession() as session:
            await session.request(
                self.config.method,
                self.config.url,
                json=payload,
                headers=headers,
            )
        
        return HookResult(action="continue")


async def mount(coordinator, config: dict | None = None):
    config = config or {}
    
    url = config.get("url")
    if not url:
        raise ValueError("url is required for hooks-notify-webhook")
    
    webhook_config = WebhookConfig(
        url=url,
        method=config.get("method", "POST"),
        headers=config.get("headers"),
        include_session_id=config.get("include_session_id", True),
        include_turn_count=config.get("include_turn_count", True),
    )
    
    hook = WebhookNotifyHook(webhook_config)
    
    coordinator.hooks.register(
        "notify:turn-complete",
        hook.handle_turn_complete,
        priority=100,
        name="hooks-notify-webhook",
    )
    
    return {"name": "hooks-notify-webhook", "url": url}
```

## Best Practices

### Do

- **Keep hooks independent** - Each hook should work on its own
- **Use `notify:turn-complete`** if you want normalized data
- **Use `orchestrator:complete`** if you need raw data or independence
- **Handle errors gracefully** - Don't fail the hook if your notification fails
- **Make configuration explicit** - Use environment variables for secrets

### Don't

- **Don't create provider registries** - Composition IS the plugin system
- **Don't require hooks-notify** - Let users choose their notification stack
- **Don't block on slow operations** - Fire and forget where possible
- **Don't emit events unless you own the namespace** - Emit `yourmodule:*` events

## Event Namespace Convention

If you emit your own events, use your module name as prefix:

```python
# Good - namespaced to your module
await coordinator.hooks.emit("notify-slack:message-sent", {...})

# Bad - polluting the notify namespace
await coordinator.hooks.emit("notify:slack-sent", {...})
```

The `notify:*` namespace is reserved for the core notify bundle.

## Testing Your Hook

```python
# test_slack_hook.py
import pytest
from unittest.mock import AsyncMock, MagicMock

async def test_slack_notification():
    # Mock coordinator
    coordinator = MagicMock()
    coordinator.hooks = MagicMock()
    coordinator.hooks.register = MagicMock()
    
    # Mount with test config
    from amplifier_module_hooks_notify_slack import mount
    result = await mount(coordinator, {
        "webhook_url": "https://hooks.slack.com/test",
        "channel": "#test",
    })
    
    assert result["name"] == "hooks-notify-slack"
    coordinator.hooks.register.assert_called_once()
```

## Questions?

- **Amplifier patterns**: Consult `amplifier:amplifier-expert`
- **Hook system details**: Consult `core:core-expert`
- **Bundle composition**: Consult `foundation:foundation-expert`
