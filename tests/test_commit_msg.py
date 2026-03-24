import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HOOK = REPO_ROOT / "hooks" / "commit-msg"


def run_hook(content, extra_env=None):
    with tempfile.TemporaryDirectory() as td:
        msg_path = Path(td) / "COMMIT_EDITMSG"
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


class CommitMsgHookTests(unittest.TestCase):
    def test_accepts_valid_conventional_commit_without_mutation_by_default(self):
        proc, content = run_hook("feat: add feature\n")

        self.assertEqual(proc.returncode, 0)
        self.assertEqual(content, "feat: add feature\n")

    def test_rejects_invalid_commit_type(self):
        proc, content = run_hook("feature: add feature\n")

        self.assertEqual(proc.returncode, 1)
        self.assertEqual(content, "feature: add feature\n")
        self.assertIn(
            "does not follow conventional commit specification",
            proc.stdout,
        )

    def test_adds_breaking_bang_without_emoji_by_default(self):
        proc, content = run_hook(
            "feat: add api\n\nBREAKING CHANGE: endpoint changed\n"
        )

        self.assertEqual(proc.returncode, 0)
        self.assertEqual(
            content,
            "feat!: add api\n\nBREAKING CHANGE: endpoint changed\n",
        )

    def test_adds_emoji_when_enabled(self):
        proc, content = run_hook(
            "feat: add feature\n",
            {"CONVENTIONAL_COMMITS_PRECOMMIT_EMOJI": "true"},
        )

        self.assertEqual(proc.returncode, 0)
        self.assertEqual(content, "feat: add feature ✨\n")

    def test_supports_legacy_noemoji_false_override(self):
        proc, content = run_hook(
            "feat: add feature\n",
            {"CONVENTIONAL_COMMITS_PRECOMMIT_NOEMOJI": "false"},
        )

        self.assertEqual(proc.returncode, 0)
        self.assertEqual(content, "feat: add feature ✨\n")

    def test_rejects_empty_commit_message_without_traceback(self):
        proc, content = run_hook("")

        self.assertEqual(proc.returncode, 1)
        self.assertEqual(content, "")
        self.assertIn("Commit message must not be empty.", proc.stdout)
        self.assertEqual(proc.stderr, "")

    def test_rejects_comment_only_commit_message_without_traceback(self):
        proc, content = run_hook("# Please enter the commit message.\n\n")

        self.assertEqual(proc.returncode, 1)
        self.assertEqual(content, "# Please enter the commit message.\n\n")
        self.assertIn("Commit message must not be empty.", proc.stdout)
        self.assertEqual(proc.stderr, "")


if __name__ == "__main__":
    unittest.main()
