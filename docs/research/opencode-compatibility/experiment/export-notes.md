# OpenCode public-session export

`export-opencode.py` transports one completed OpenCode session to a public JSON
artifact. It runs `opencode export` with the requested project as both the child
working directory and `PWD`, collects stdout through a PTY to avoid pipe-size
truncation, parses the full document in memory, and applies the recursive
`clean()` sanitizer from `run-opencode.py` before writing anything.

```sh
python3 docs/research/opencode-compatibility/experiment/export-opencode.py \
  --cwd /absolute/path/to/project \
  --session ses_example \
  --out /absolute/path/to/session.public.json
```

The destination must not exist. The default timeout is 30 seconds and can be
changed with `--timeout`. Raw export bytes and stderr remain in memory and are
never persisted. This helper is evidence transport only; it does not invoke a
model, grade session semantics, or replace an evaluation harness.
