# Agent Instructions

## Quickstart & Environment

- **Python**: `>=3.10` (CPython 3.11 recommended).
- **Setup**: `uv venv --python 3.11 && uv pip install -e ".[dev]"`
- **Run Game**: `python main.py` (entry point `src.app.GameApp`).
- **Run Tests**: `pytest` or `.venv/bin/pytest` (automatically executes headless via `tests/conftest.py`).

## Codebase Architecture

- **`src/`**: All active application logic and systems.
  - `src/core/`: Engine services (`AssetManager`, `SaveManager`, `Bonus`, `World`).
  - `src/entities/`: Game actors (`Tower` variants, `Enemy`, `Bullet`).
  - `src/scenes/`: State-driven screens (`SceneManager`, `MainMenuScene`, `GameplayScene`, `ResearchScene`, `LevelSelectScene`).
  - `src/data/`: Static configurations and tables (`constants.py`, `tower_data.py`, `enemy_data.py`, `research_data.py`).
  - `src/ui/`: UI widgets and helpers (`Button`, `HealthBar`, `draw_text`).
- **Root `.py` files**: Minimal re-export shims for backwards compatibility. Do not write new logic here.
- **`assets/data.json`**: Runtime save file (ignored by git). Always manipulate via `SaveManager`.

## Subagents & Sandbox Guidelines

- **Worktree Boundary**: The security sandbox restricts disk access strictly to the project root. Never create worktrees in `../` outside this workspace. Use in-workspace worktrees under `.worktrees/<branch>` (ignored in `.gitignore`).
- **Implementer Subagents**: Always delegate ticket implementation to subagents (`TypeName: "self"` with write tools) rather than running sequentially on the main coordinator turn.
- **Review Subagents**: When invoking `research` subagents (read-only), provide diffs and specs directly as file paths or prompt attachments; do not rely on subagents calling shell CLI commands.

## Agent Skills & Domain Reference

- **Issue Tracker**: GitHub issues tracked via `gh` CLI. See `docs/agents/issue-tracker.md`.
- **Triage Labels**: Canonical triage label vocabulary. See `docs/agents/triage-labels.md`.
- **Domain Docs**: Unified vocabulary (`Money`, `Coin`, `Research`, `Bonus`, `Wave`, `World`). See `GLOSSARY.md` and `docs/agents/domain.md`.
