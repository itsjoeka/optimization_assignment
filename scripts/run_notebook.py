"""Execute a notebook in place, so its committed copy carries real outputs.

Usage:  python3 scripts/run_notebook.py notebooks/05_manuscript_results.ipynb

Kept as a file rather than an inline `python3 -c` one-liner: quoting a
multi-line program through the shell silently mangled it once already, and the
wrapper still exited 0, which made an unexecuted notebook look executed.
"""
from __future__ import annotations

import pathlib
import sys

import nbformat
from nbclient import NotebookClient

TIMEOUT_PER_CELL = 2400


def main(path_str: str) -> int:
    path = pathlib.Path(path_str).resolve()
    if not path.exists():
        print(f"no such notebook: {path}")
        return 2

    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(
        nb,
        timeout=TIMEOUT_PER_CELL,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
        allow_errors=False,
    )
    client.execute()
    nbformat.write(nb, path)

    # Verify rather than trust: an exit code of 0 is not evidence that cells ran.
    check = nbformat.read(path, as_version=4)
    code = [c for c in check.cells if c.cell_type == "code"]
    empty = [i for i, c in enumerate(code) if not c.get("outputs")]
    errors = [i for i, c in enumerate(code)
              if any(o.get("output_type") == "error" for o in c.get("outputs", []))]

    print(f"{len(code)} code cells | {len(empty)} without output | {len(errors)} with errors")
    if errors:
        print(f"FAILED: cells with errors at indices {errors}")
        return 1
    if empty:
        print(f"FAILED: cells produced no output at indices {empty}")
        return 1
    print(f"OK: {path.name} executed and written with outputs")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
