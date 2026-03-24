# conventional-commits-precommit

A `commit-msg` hook for `pre-commit`-compatible runners such as `pre-commit` and `prek`.

The hook validates commit messages against a conventional-commit style and can optionally rewrite the header to:

- add `!` when the message contains a `BREAKING CHANGE:` footer
- optionally append a matching emoji when emoji mode is enabled

## Hook

| id | stage | description |
| --- | --- | --- |
| `check-commit-msg` | `commit-msg` | Validate conventional commit headers and optionally append emojis |

## Installation

Add this repository to your `.pre-commit-config.yaml` or equivalent `prek` config:

```yaml
repos:
  - repo: https://github.com/kdheepak/conventional-commits-precommit
    rev: v0.4.0
    hooks:
      - id: check-commit-msg
```

Then install the `commit-msg` hook type:

```bash
pre-commit install --hook-type commit-msg
```

If you use `prek`, install the repository's `commit-msg` hook with the corresponding `prek` install command.

## Checks

The hook reads the first non-empty, non-comment line from the commit message and expects a header in this shape:

```text
type: subject
type(scope): subject
type!: subject
type(scope)!: subject
```

Supported commit types:

`new`, `feat`, `fix`, `revert`, `build`, `chore`, `ci`, `docs`, `perf`, `refactor`, `style`, `test`, `wip`, `fixup`

Accepted examples:

```text
feat: add release workflow
fix(parser): preserve trailing colon
refactor!: drop deprecated CLI path
docs(readme): document emoji mode
```

Rejected examples:

```text
feature: add release workflow
feat add release workflow
chore(scope) add release workflow
```

Empty or comment-only commit messages are rejected as well.

## Breaking Changes

If the commit message contains a `BREAKING CHANGE:` footer and the header does not already include `!`, the hook rewrites the header to include it.

Example:

```text
feat: redesign API

BREAKING CHANGE: rename the public client constructor
```

becomes:

```text
feat!: redesign API

BREAKING CHANGE: rename the public client constructor
```

## Emoji Mode

By default, valid commit headers are left unchanged.

To append an emoji that matches the commit type, enable:

```bash
export CONVENTIONAL_COMMITS_PRECOMMIT_EMOJI=true
```

Example:

```text
feat: add release workflow
```

becomes:

```text
feat: add release workflow ✨
```

If the commit is breaking, the hook appends both the breaking-change emoji and the type emoji.

## Development

Run the test suite with:

```bash
mise run test
```

This uses:

```bash
uv run --with pytest pytest
```

## Reference

Conventional Commits: https://www.conventionalcommits.org/
