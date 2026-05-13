# Core Stability Refactor Design

## Goal

Refactor the runtime into smaller, easier-to-maintain modules while preserving the current interactive flow. The work focuses on reliability, observability, configuration hygiene, and graceful shutdown. It does not add new automation behavior or expand high-risk Discord actions.

## Scope

- Move hardcoded runtime settings out of the Discord client class.
- Replace silent exception handling with useful logs that do not expose full tokens.
- Split the monolithic script into focused modules.
- Keep the existing launch path through `self-bot.py`.
- Improve shutdown so client close operations run predictably.

## Non-Goals

- No new Discord automation features.
- No changes intended to evade platform limits, checks, or enforcement.
- No expansion of reaction, messaging, or account-control behavior.
- No dependency changes unless required for basic correctness.

## Architecture

The refactor introduces a `voicebot` package:

- `voicebot/config.py`: environment-backed settings and small parsing helpers.
- `voicebot/logging_setup.py`: logging configuration and noisy third-party logger suppression.
- `voicebot/client.py`: `VoiceClone`, Discord compatibility patch, voice join, state toggles, and message owner checks.
- `voicebot/manager.py`: token loading, bot lifecycle, channel assignment, batch operations, auto-room flow, and shutdown.
- `voicebot/cli.py`: banner, prompts, mode selection, and control menu.
- `self-bot.py`: thin entrypoint that runs the CLI.

## Configuration

`OWNER_ID` should be read from the `OWNER_ID` environment variable. If unset or invalid, owner-only chat echo commands stay disabled and the program logs a warning. `TOKENS_FILE` may override the default `tokens.txt` path.

This avoids requiring users to edit source code for sensitive configuration.

## Error Handling

Token display is always masked, for example `abc123...`. Fetch, join, rename, and message-send failures should be logged with context. Broad exception handlers remain only around network or Discord API boundaries, where the program must keep running, but they must no longer be empty.

## Data Flow

1. CLI configures logging and loads settings.
2. Manager loads tokens from the configured token file.
3. CLI prompts for mode, delay, and channel IDs.
4. Manager creates one `VoiceClone` per token and starts each client task.
5. CLI control loop dispatches batch operations through Manager.
6. Shutdown closes every started client and waits briefly for cleanup.

## Testing

Because live Discord login requires real credentials and network access, verification is limited to local checks:

- Python syntax compilation for all project Python files.
- Import check for the new package modules.
- Review of source references to confirm `OWNER_ID` is no longer hardcoded inside `VoiceClone`.

