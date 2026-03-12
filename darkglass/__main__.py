import argparse

from .main import app


def main() -> None:
    """Entry point for the :command:`darkglass` console script.

    Running ``darkglass`` will start the server in the current working
    directory.  ``--dev`` toggles the development mode, which simply
    enables :param:`reload` on :mod:`uvicorn` so that the process will
    restart when Python source files change.

    Additional command line options mirror the arguments accepted by
    :func:`uvicorn.run` so that users have a simple way to override the
    host/port without needing their own wrapper script.

    No other behaviour is bundled; the package itself does not depend on
    :mod:`click` or similar so we stick with :mod:`argparse`.
    """

    parser = argparse.ArgumentParser(prog="darkglass")
    parser.add_argument(
        "--dev",
        action="store_true",
        help="run the server in development mode (" "uvicorn --reload)",
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="host to bind the server to (default 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="port to listen on (default 8000)",
    )

    args = parser.parse_args()

    import uvicorn

    uvicorn.run(app, host=args.host, port=args.port, reload=args.dev)


if __name__ == "__main__":
    main()
