import os
import pathlib
import subprocess
import sys
import tempfile


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
HOOK = REPO_ROOT / "hooks" / "commit-msg"


def run_hook(
    content: str, extra_env: dict[str, str] | None = None
) -> tuple[subprocess.CompletedProcess[str], str]:
    with tempfile.TemporaryDirectory() as td:
        msg_path = pathlib.Path(td) / "COMMIT_EDITMSG"
        msg_path.write_text(content)
        env = os.environ.copy()
        if extra_env:
            env.update(extra_env)
        proc = subprocess.run(
            [sys.executable, str(HOOK), str(msg_path)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            env=env,
        )
        return proc, msg_path.read_text()


def test_accepts_valid_conventional_commit_without_mutation_by_default():
    proc, content = run_hook("feat: add feature\n")

    assert proc.returncode == 0
    assert content == "feat: add feature\n"


def test_accepts_scope_with_dot():
    proc, content = run_hook(
        "fix(web.config): update cache dir path in aspNetCore arguments\n"
    )

    assert proc.returncode == 0
    assert content == "fix(web.config): update cache dir path in aspNetCore arguments\n"


def test_rejects_invalid_commit_type():
    proc, content = run_hook("feature: add feature\n")

    assert proc.returncode == 1
    assert content == "feature: add feature\n"
    assert "does not follow conventional commit specification" in proc.stdout


def test_adds_breaking_bang_without_emoji_by_default():
    proc, content = run_hook("feat: add api\n\nBREAKING CHANGE: endpoint changed\n")

    assert proc.returncode == 0
    assert content == "feat!: add api\n\nBREAKING CHANGE: endpoint changed\n"


def test_adds_emoji_when_enabled():
    proc, content = run_hook(
        "feat: add feature\n",
        {"CONVENTIONAL_COMMITS_PRECOMMIT_EMOJI": "true"},
    )

    assert proc.returncode == 0
    assert content == "feat: add feature ✨\n"


def test_supports_legacy_noemoji_false_override():
    proc, content = run_hook(
        "feat: add feature\n",
        {"CONVENTIONAL_COMMITS_PRECOMMIT_NOEMOJI": "false"},
    )

    assert proc.returncode == 0
    assert content == "feat: add feature ✨\n"


def test_rejects_empty_commit_message_without_traceback():
    proc, content = run_hook("")

    assert proc.returncode == 1
    assert content == ""
    assert "Commit message must not be empty." in proc.stdout
    assert proc.stderr == ""


def test_rejects_comment_only_commit_message_without_traceback():
    proc, content = run_hook("# Please enter the commit message.\n\n")

    assert proc.returncode == 1
    assert content == "# Please enter the commit message.\n\n"
    assert "Commit message must not be empty." in proc.stdout
    assert proc.stderr == ""
