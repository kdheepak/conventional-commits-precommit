# Conventional commits precommit hook

```yaml
# Make sure to set the default_stages in your config file
# to prevent installing hooks multiple times inadvertently
default_stages: [commit]

repos:
  - repo: https://github.com/kdheepak/conventional-commits-precommit
    rev: v0.3.9
    hooks:
      - id: check-commit-msg
```

Then run `pre-commit install -t commit-msg` and you're ready to go.

If you don't want emojis to be auto appended, use the environment variable `CONVENTIONAL_COMMITS_PRECOMMIT_NOEMOJI=true`.
