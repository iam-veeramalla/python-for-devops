"""Safely update a KEY=VALUE entry in a server configuration file."""

import argparse
import difflib
import os
import stat
import sys
import tempfile
from pathlib import Path


class ConfigUpdateError(ValueError):
    """Raised when a configuration change cannot be made unambiguously."""


def _validate_arguments(key, value):
    if not key or not key.strip():
        raise ConfigUpdateError("configuration key must not be empty")
    if "=" in key:
        raise ConfigUpdateError("configuration key must not contain '='")
    if "\n" in key or "\r" in key:
        raise ConfigUpdateError("configuration key must be a single line")
    if "\n" in value or "\r" in value:
        raise ConfigUpdateError("configuration value must be a single line")


def _without_line_ending(line):
    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n") or line.endswith("\r"):
        return line[:-1], line[-1:]
    return line, ""


def _build_updated_content(original, key, value):
    lines = original.splitlines(keepends=True)
    matches = []

    for index, line in enumerate(lines):
        body, newline = _without_line_ending(line)
        stripped = body.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith(";"):
            continue

        left, separator, _ = body.partition("=")
        if separator and left.strip() == key:
            matches.append((index, left, newline, body.partition("=")[2]))

    if not matches:
        raise ConfigUpdateError(f"configuration key {key!r} was not found")
    if len(matches) > 1:
        raise ConfigUpdateError(
            f"configuration key {key!r} appears more than once; refusing to guess"
        )

    index, left, newline, old_value = matches[0]
    right = lines[index].partition("=")[2]
    value_prefix = right[: len(right) - len(right.lstrip(" \\t"))]
    lines[index] = f"{left}={value_prefix}{value}{newline}"
    return "".join(lines), old_value


def _atomic_replace(path, content):
    """Replace an existing file atomically, keeping its mode where supported."""
    original_mode = stat.S_IMODE(path.stat().st_mode)
    temp_path = None
    file_descriptor = None

    try:
        file_descriptor, temp_name = tempfile.mkstemp(
            prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
        )
        temp_path = Path(temp_name)
        with os.fdopen(file_descriptor, "wb") as temporary_file:
            file_descriptor = None
            temporary_file.write(content.encode("utf-8"))
            temporary_file.flush()
            os.fsync(temporary_file.fileno())

        os.chmod(temp_path, original_mode)
        os.replace(temp_path, path)
        temp_path = None
    finally:
        if file_descriptor is not None:
            os.close(file_descriptor)
        if temp_path is not None:
            try:
                temp_path.unlink()
            except OSError:
                pass


def update_server_config(file_path, key, value, apply=False):
    """Propose an update, writing it only when apply=True.

    Returns (old_value, original_content, updated_content). File read and write
    errors are allowed to propagate so the CLI can report them accurately.
    """
    _validate_arguments(key, value)
    path = Path(file_path)
    original_bytes = path.read_bytes()
    try:
        original = original_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ConfigUpdateError("configuration file must be UTF-8 text") from error

    updated, old_value = _build_updated_content(original, key, value)
    if apply:
        _atomic_replace(path, updated)
    return old_value, original, updated


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Safely update one exact KEY=VALUE entry in a config file."
    )
    parser.add_argument("file", help="existing KEY=VALUE configuration file")
    parser.add_argument("key", help="exact configuration key to update")
    parser.add_argument("value", help="new single-line value")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="write the change (default: display a dry-run diff only)",
    )
    args = parser.parse_args(argv)

    try:
        _validate_arguments(args.key, args.value)
        old_value, original, updated = update_server_config(
            args.file, args.key, args.value, apply=args.apply
        )
    except ConfigUpdateError as error:
        parser.error(str(error))
    except OSError as error:
        print(f"Error: could not update {args.file!r}: {error}", file=sys.stderr)
        return 1

    if args.apply:
        print(
            f"Updated {args.key} in {args.file}: "
            f"{old_value!r} -> {args.value!r}"
        )
    else:
        print(
            f"Dry run: would update {args.key} in {args.file}: "
            f"{old_value!r} -> {args.value!r}"
        )
        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            updated.splitlines(keepends=True),
            fromfile=args.file,
            tofile=f"{args.file} (proposed)",
        )
        sys.stdout.writelines(diff)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
