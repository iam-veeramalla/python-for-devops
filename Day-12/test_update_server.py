"""Unit tests for the safe server configuration updater."""

import contextlib
import io
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import update_server


class UpdateServerConfigTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.config_path = Path(self.temp_dir.name) / "server.conf"

    def write_config(self, content):
        self.config_path.write_bytes(content.encode("utf-8"))

    def test_updates_existing_key(self):
        self.write_config("MAX_CONNECTIONS=100\n")
        old_value, _, updated = update_server.update_server_config(
            self.config_path, "MAX_CONNECTIONS", "600"
        )
        self.assertEqual(old_value, "100")
        self.assertEqual(updated, "MAX_CONNECTIONS=600\n")
        self.assertEqual(self.config_path.read_text(), "MAX_CONNECTIONS=100\n")

    def test_does_not_match_key_prefix(self):
        original = "MAX_CONNECTIONS_EXTRA=25\n"
        self.write_config(original)
        with self.assertRaisesRegex(update_server.ConfigUpdateError, "not found"):
            update_server.update_server_config(
                self.config_path, "MAX_CONNECTIONS", "600"
            )
        self.assertEqual(self.config_path.read_text(), original)

    def test_preserves_comments_and_unrelated_settings(self):
        original = (
            "# Example server configuration\n"
            "PORT=8080\n"
            "  MAX_CONNECTIONS = 100\n"
            "; keep this comment\n"
            "LOG_LEVEL=INFO\n"
        )
        self.write_config(original)
        _, _, updated = update_server.update_server_config(
            self.config_path, "MAX_CONNECTIONS", "600"
        )
        self.assertEqual(
            updated,
            (
                "# Example server configuration\n"
                "PORT=8080\n"
                "  MAX_CONNECTIONS = 600\n"
                "; keep this comment\n"
                "LOG_LEVEL=INFO\n"
            ),
        )

    def test_value_can_contain_equals(self):
        self.write_config("CONNECTION_STRING=old\n")
        _, _, updated = update_server.update_server_config(
            self.config_path, "CONNECTION_STRING", "host=db;options=a=b"
        )
        self.assertEqual(updated, "CONNECTION_STRING=host=db;options=a=b\n")

    def test_missing_key_fails_clearly(self):
        self.write_config("PORT=8080\n")
        with self.assertRaisesRegex(update_server.ConfigUpdateError, "not found"):
            update_server.update_server_config(self.config_path, "MISSING", "value")

    def test_duplicate_active_key_fails_safely(self):
        self.write_config("# MAX_CONNECTIONS=10\nMAX_CONNECTIONS=10\nMAX_CONNECTIONS=20\n")
        with self.assertRaisesRegex(update_server.ConfigUpdateError, "more than once"):
            update_server.update_server_config(
                self.config_path, "MAX_CONNECTIONS", "600"
            )

    def test_preserves_crlf_and_missing_final_newline(self):
        original = b"PORT=8080\r\nMAX_CONNECTIONS=100"
        self.config_path.write_bytes(original)
        _, _, updated = update_server.update_server_config(
            self.config_path, "MAX_CONNECTIONS", "600"
        )
        self.assertEqual(updated.encode("utf-8"), b"PORT=8080\r\nMAX_CONNECTIONS=600")

    def test_dry_run_cli_leaves_file_unchanged(self):
        original = "MAX_CONNECTIONS=100\nPORT=8080\n"
        self.write_config(original)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = update_server.main(
                [str(self.config_path), "MAX_CONNECTIONS", "600"]
            )
        self.assertEqual(result, 0)
        self.assertEqual(self.config_path.read_text(), original)
        self.assertIn("Dry run: would update", output.getvalue())
        self.assertIn("-MAX_CONNECTIONS=100", output.getvalue())
        self.assertIn("+MAX_CONNECTIONS=600", output.getvalue())

    def test_apply_cli_changes_only_requested_key(self):
        original = "# keep\nMAX_CONNECTIONS=100\nPORT=8080\n"
        self.write_config(original)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = update_server.main(
                [
                    str(self.config_path),
                    "MAX_CONNECTIONS",
                    "600",
                    "--apply",
                ]
            )
        self.assertEqual(result, 0)
        self.assertEqual(
            self.config_path.read_text(), "# keep\nMAX_CONNECTIONS=600\nPORT=8080\n"
        )
        self.assertIn("Updated MAX_CONNECTIONS", output.getvalue())

    def test_missing_file_returns_error_and_is_not_created(self):
        missing_path = Path(self.temp_dir.name) / "missing.conf"
        error_output = io.StringIO()
        with contextlib.redirect_stderr(error_output):
            result = update_server.main([str(missing_path), "KEY", "value"])
        self.assertEqual(result, 1)
        self.assertFalse(missing_path.exists())
        self.assertIn("Error:", error_output.getvalue())
        self.assertNotIn("Updated ", error_output.getvalue())

    def test_invalid_keys_are_rejected_by_cli(self):
        self.write_config("KEY=value\n")
        for invalid_key in ("", "BAD=KEY"):
            with self.subTest(key=invalid_key):
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as error:
                        update_server.main(
                            [str(self.config_path), invalid_key, "new-value"]
                        )
                self.assertEqual(error.exception.code, 2)
        self.assertEqual(self.config_path.read_text(), "KEY=value\n")

    def test_newline_values_are_rejected(self):
        self.write_config("KEY=value\n")
        with self.assertRaisesRegex(update_server.ConfigUpdateError, "single line"):
            update_server.update_server_config(self.config_path, "KEY", "one\ntwo")
        self.assertEqual(self.config_path.read_text(), "KEY=value\n")

    def test_import_does_not_modify_a_config_file(self):
        original = "MAX_CONNECTIONS=100\n"
        self.write_config(original)
        module_directory = Path(update_server.__file__).resolve().parent
        environment = os.environ.copy()
        environment["PYTHONPATH"] = str(module_directory)
        result = subprocess.run(
            [sys.executable, "-c", "import update_server"],
            cwd=self.temp_dir.name,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.config_path.read_text(), original)


if __name__ == "__main__":
    unittest.main()
