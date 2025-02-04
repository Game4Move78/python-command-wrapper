#!/usr/bin/env python3

import os
import sys
import subprocess

LOCAL_PATH = "{local_path}"

def find_binary():
    """Finds the binary, preferring the system PATH if available."""

    if os.path.isabs(LOCAL_PATH):
        local_binary = LOCAL_PATH
    else:
        repo_dir = os.path.dirname(os.path.abspath(__file__))
        repo_dir = os.path.dirname(repo_dir)
        repo_dir = os.path.dirname(repo_dir)
        local_binary = os.path.join(repo_dir, LOCAL_PATH)

    if os.path.exists(local_binary) and os.access(local_binary, os.X_OK):
        return local_binary

    print(f"Error: Binary '{{local_binary}}' not executable.", file=sys.stderr)
    sys.exit(1)

def main():
    """Executes the binary and forwards all arguments."""
    binary = find_binary()
    if os.name == "posix":
        os.execvp(binary, (binary, *sys.argv[1:]))
    else:
        subprocess.run([binary] + sys.argv[1:], check=True)

if __name__ == "__main__":
    main()
