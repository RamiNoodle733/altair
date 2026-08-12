import pytest

from altair.utils import _show


def test_open_html_in_browser_closes_server(monkeypatch):
    events = []

    class Browser:
        def open(self, url):
            events.append(("open", url))

    class FakeServer:
        server_port = 4321

        def __init__(self, address, handler):
            events.append(("init", address, handler.__name__))

        def __enter__(self):
            events.append("enter")
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            events.append("exit")

        def handle_request(self):
            events.append("handle")

    monkeypatch.setattr(_show.webbrowser, "get", lambda _: Browser())
    monkeypatch.setattr(_show, "HTTPServer", FakeServer)

    _show.open_html_in_browser("<p>hello</p>")

    assert events[1:] == [
        "enter",
        ("open", "http://127.0.0.1:4321"),
        "handle",
        "exit",
    ]


def test_open_html_in_browser_closes_server_when_browser_open_fails(monkeypatch):
    events = []

    class Browser:
        def open(self, url):
            events.append(("open", url))
            raise RuntimeError("browser failed")

    class FakeServer:
        server_port = 4321

        def __init__(self, address, handler):
            events.append(("init", address, handler.__name__))

        def __enter__(self):
            events.append("enter")
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            events.append(("exit", exc_type))

        def handle_request(self):
            events.append("handle")

    monkeypatch.setattr(_show.webbrowser, "get", lambda _: Browser())
    monkeypatch.setattr(_show, "HTTPServer", FakeServer)

    with pytest.raises(RuntimeError, match="browser failed"):
        _show.open_html_in_browser("<p>hello</p>")

    assert events[1:] == [
        "enter",
        ("open", "http://127.0.0.1:4321"),
        ("exit", RuntimeError),
    ]
