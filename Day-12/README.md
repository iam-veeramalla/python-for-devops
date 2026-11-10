# Day 12: Safe server configuration updates

`update_server.py` updates one existing entry in a simple `KEY=VALUE` configuration file. It matches the exact key before the first `=`, preserves other lines and comments, and refuses to update a missing or duplicate key.

## Sample configuration

Save this placeholder example as `Day-12/server.conf` before trying the commands:

```ini
# Example settings; replace values for your own local exercise.
MAX_CONNECTIONS=500
PORT=8080
LOG_LEVEL=INFO
```

## Dry run first

From the repository root, preview the change without editing the file:

```sh
python Day-12/update_server.py Day-12/server.conf MAX_CONNECTIONS 600
```

Dry-run mode is the default. The script prints the old and proposed values plus a diff. It does not modify the configuration.

To write the change, explicitly pass `--apply`:

```sh
python Day-12/update_server.py Day-12/server.conf MAX_CONNECTIONS 600 --apply
```

The script writes a temporary file in the same directory, preserves the original file mode where supported, and replaces the file atomically where the operating system supports it. It will not create a missing configuration file.

Exact-key matching prevents a request for `MAX_CONNECTIONS` from also changing a setting such as `MAX_CONNECTIONS_EXTRA`. Blank lines and comment lines are ignored, and duplicate active keys fail safely instead of guessing. Values may contain `=`; keys may not.

## Run the tests

From the repository root:

```sh
python -m unittest discover -s Day-12 -p "test_*.py" -v
python -m py_compile Day-12/update_server.py Day-12/test_update_server.py
```

The tests use temporary files only and require no cloud credentials, network access, or elevated permissions.
