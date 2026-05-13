# Blocked: Claude Code Task Delegation

## Date

2026-05-13

## Status

Blocked

## Context

`claude` is available on PATH, but the process environment does not contain `ANTHROPIC_API_KEY`.

## Impact

Codex cannot delegate `TASK-001` to Claude Code without authentication. No Claude Code report has been fabricated.

## Required follow-up

- Set `ANTHROPIC_API_KEY` in the process environment outside the repository.
- Re-run:

```powershell
conda run -p E:\anaconda3\envs\pytorch-clean python tools/run_claude_task.py tasks/active/TASK-001.md
```

## Security note

Do not write the real API key into `.env`, task cards, reports, logs, or commits.

