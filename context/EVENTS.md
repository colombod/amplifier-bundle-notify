# Amplifier Events for Notifications

This document describes the Amplifier events relevant to notification hooks.

## Turn Completion Events

### `orchestrator:complete`

**The primary event for turn completion notifications.**

Emitted when the orchestrator finishes processing a user prompt and is ready for the next input.

```python
await hooks.emit(
    "orchestrator:complete",
    {
        "orchestrator": "loop-streaming",
        "turn_count": 3,
        "status": "success"
    }
)
```

| Field | Type | Description |
|-------|------|-------------|
| `orchestrator` | str | Name of the orchestrator module |
| `turn_count` | int | Number of LLM iterations in this turn |
| `status` | str | "success" or "incomplete" |

**Emitted by:**
- `loop-basic` ✅
- `loop-streaming` ✅

### `prompt:complete`

Alternative event for prompt processing completion.

```python
await hooks.emit(
    "prompt:complete",
    {
        "response_preview": "I've completed...",
        "length": 1234
    }
)
```

**Emitted by:**
- `loop-basic` ✅
- `loop-streaming` ❌ (not emitted)

**Recommendation:** Use `orchestrator:complete` for broader compatibility.

## Session Events

### `session:start`

Emitted when a session begins.

```python
await hooks.emit("session:start", {"prompt": "Hello"})
```

### `session:end`

Emitted when a session ends.

```python
await hooks.emit("session:end", {})
```

## Error Events

### `tool:error`

Emitted when a tool execution fails.

```python
await hooks.emit(
    "tool:error",
    {
        "tool_name": "bash",
        "error": "Command failed with exit code 1",
        "tool_call_id": "call_123"
    }
)
```

### `provider:error`

Emitted when an LLM provider call fails.

```python
await hooks.emit(
    "provider:error",
    {
        "provider": "anthropic",
        "error": "Rate limit exceeded"
    }
)
```

## Streaming Events

### `content_block:start` / `content_block:delta` / `content_block:end`

For real-time streaming UI updates (not typically used for notifications).

## Event Selection Guide

| Use Case | Recommended Event |
|----------|-------------------|
| "Assistant ready for input" | `orchestrator:complete` |
| "Long operation finished" | `orchestrator:complete` with `turn_count` filter |
| "Tool execution failed" | `tool:error` |
| "Session finished" | `session:end` |
| "LLM error occurred" | `provider:error` |

## Hook Priority

When registering notification hooks, use a high priority number (runs later) so core functionality executes first:

```python
coordinator.hooks.register(
    "orchestrator:complete",
    handler,
    priority=100  # High number = runs after priority=10 hooks
)
```
