#!/usr/bin/env python

import os
import platform
import socket
import subprocess
import sys

import api.config
from api.config import PROJECT_DIR


def find_free_port(start_port: int = 5000, end_port: int = 5042):
    """
    Scans for a free TCP port in a given range.

    Args:
        start_port: The first port to check.
        end_port: The last port to check.

    Returns:
        The first available port number, or None if no port is free.
    """
    print(f"Scanning for an available port from {start_port} to {end_port}...")
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            print(f"Port {port} is in use, trying next...")
            continue
    return None


def _check_help():
    if len(sys.argv) > 1 and sys.argv[1] in {"help", "--help", "-h"}:
        return True
    return False


def cli_entrypoint(model_name="auto"):
    cli_help = \
        """
        Convenience tool to launch flask server using gunicorn.

        In the simplest case, you can simply run:
        $ ark-run

        This will automatically detect the model in the current environment and launch the server.
        The model must be installed in the current environment; this can be done simply with:

        $ pip install 'ark[mirai]'

        or 

        $ pip install 'ark[sybil]'

        It is not recommended to install both models in the same environment, 
        as they have slightly different dependencies.


        If you'd like to specify a model, you can run:
        $ ark-run <model_name>

        where <model_name> is one of "empty", "mirai", or "sybil".

        $ ark-run empty

        will launch the server with an empty model, which is useful for testing the API.
        """

    if _check_help():
        print(cli_help)
        exit(0)

    if len(sys.argv) > 1:
        model_name = sys.argv[1]

    api.config.set_config_by_name(model_name)

    port = find_free_port()
    if port is None:
        print("Error: Could not find an available port in the range 5000-5020.", file=sys.stderr)
        sys.exit(1)

    print(f"Found available port. Launching server on port {port}...")

    LOGLEVEL_KEY = "LOG_LEVEL"
    loglevel = os.environ.get(LOGLEVEL_KEY, "INFO")
    threads = os.environ.get("ARK_THREADS", "4")
    if platform.system() == "Windows":
        args = ["waitress-serve",
                "--channel-timeout", "3600",
                "--threads", threads,
                "--port", str(port),
                "--call", "main:create_app"]

    else:
        args = ["gunicorn",
                "--bind", f"0.0.0.0:{port}",
                "--timeout", "0",
                "--threads", threads,
                "--log-level", loglevel,
                "--access-logfile", "-",
                "main:create_app()"]

    proc = subprocess.run(args, stdout=None, stderr=None, text=True, cwd=PROJECT_DIR)




def cli_entrypoint_sybil():
    import sybil
    _ = sybil
    cli_entrypoint("sybil")

#
#

if __name__ == "__main__":
    cli_entrypoint_sybil()