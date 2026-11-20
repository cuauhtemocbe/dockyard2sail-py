import os
import socket
import threading
import time
from collections.abc import Iterator
from typing import Any

import pytest
import uvicorn

from app.main import app

SERVER_START_TIMEOUT_SECONDS = 10


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    # pytest-playwright's session-scoped sync Playwright keeps an event loop
    # running in the main thread from the first browser test until the end of
    # the session; pytest-asyncio tests that run after it error out. Run the
    # browser tests last (the sort is stable, so the rest keeps its order).
    items.sort(
        key=lambda item: (
            isinstance(item, pytest.Function) and "page" in item.fixturenames
        )
    )


@pytest.fixture(scope="session")
def browser_type_launch_args(
    browser_type_launch_args: dict[str, Any],
) -> dict[str, Any]:
    # Chromium refuses to start its sandbox as root, and the dev container
    # (Dockerfile.dev) runs as root. A non-root run keeps the sandbox on.
    if os.geteuid() == 0:
        return {**browser_type_launch_args, "args": ["--no-sandbox"]}
    return browser_type_launch_args


@pytest.fixture(scope="session")
def live_server_url() -> Iterator[str]:
    """Serve the real app over HTTP on a free port, for browser tests."""
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(app, log_level="warning"))
    thread = threading.Thread(
        target=server.run, kwargs={"sockets": [sock]}, daemon=True
    )
    thread.start()

    deadline = time.monotonic() + SERVER_START_TIMEOUT_SECONDS
    while not server.started:
        if time.monotonic() > deadline:
            raise RuntimeError("live server did not start in time")
        time.sleep(0.05)

    yield f"http://127.0.0.1:{port}"

    server.should_exit = True
    thread.join(timeout=SERVER_START_TIMEOUT_SECONDS)
    sock.close()
