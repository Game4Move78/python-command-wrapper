#!/usr/bin/env python3

import os
import argparse
import shutil
import subprocess
import sys
import tempfile

REPO_DIR = os.path.dirname(os.path.abspath(__file__))

def format_template(fn, **kwds):
    with open(fn, "r") as fin:
        template = fin.read()

    return template.format(**kwds)

def write_template(template_fn, output_fn=None, output_dir="python", **kwds):
    if output_fn is None:
        output_fn = template_fn
    content = format_template(os.path.join(REPO_DIR, "templates", template_fn), **kwds)
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, output_fn), "w") as fout:
        fout.write(content)

def binary_module_name(binary_name):
    module_name = binary_name.replace("-", "_")
    return module_name

def generate_wrapper(binary_name, local_path):
    """Generates a Python wrapper script for the given binary."""

    module_name = binary_module_name(binary_name)
    module_dir = os.path.join("wrappers", module_name)

    write_template("wrapper.py", f"{module_name}.py", local_path=local_path, output_dir=module_dir)
    write_template("pyproject.toml", output_name=binary_name, module_name=module_name, output_dir=module_dir)
    write_template("setup.py", output_name=binary_name, module_name=module_name, output_dir=module_dir)

    return module_dir

def install_wrapper(binary, local_path, use_poetry):
    if local_path is None:
        local_path = binary
    if use_poetry:
        try:
            import poetry
        except ImportError:
            print("Poetry not installed. Run `pip install poetry`.", file=sys.stderr)
            sys.exit(1)

    module_dir = generate_wrapper(binary, local_path)

    if use_poetry:
        cmd = ["poetry", "install", "--directory", module_dir]
    else:
        cmd = ["pip", "install", "-e", module_dir]

    subprocess.run(cmd, check=True)

def uninstall_wrapper(binary):

    import importlib

    module_name = binary_module_name(binary)

    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"{module_name} not installed", file=sys.stderr)
        sys.exit(1)

    module_dir = os.path.dirname(module.__file__)
    wrappers_dir = os.path.dirname(module_dir)

    cmd = ["pip", "uninstall", "-y", module_name]
    subprocess.run(cmd, check=True)
    shutil.rmtree(module_dir)

    if len(os.listdir(wrappers_dir)) == 0:
        os.rmdir(wrappers_dir)

def parse_args():
    parser = argparse.ArgumentParser(description="Generate a Python wrapper for a binary.")
    parser.add_argument("binary", help="The binary.")
    parser.add_argument("local_path", default=None,
                        help="Relative path to the binary if not found in PATH.", nargs="?")
    parser.add_argument("--poetry", action='store_true', default=False)
    parser.add_argument("--uninstall", action='store_true', default=False)

    return parser.parse_args()

def main():
    args = parse_args()
    if args.uninstall:
        uninstall_wrapper(args.binary)
    else:
        install_wrapper(args.binary, args.local_path, args.use_poetry)

if __name__ == "__main__":
    main()
