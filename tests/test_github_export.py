import base64
import types

import pytest

from translator.generators.github_export import push_text_file_to_github


class _Resp:
    def __init__(self, status_code: int, payload: dict | None = None, text: str = "") -> None:
        self.status_code = status_code
        self._payload = payload or {}
        self.text = text

    def json(self) -> dict:
        return self._payload


def test_push_text_file_to_github_requires_token(monkeypatch) -> None:
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    with pytest.raises(RuntimeError):
        push_text_file_to_github("o/r", "a.py", "print(1)", "msg")


def test_push_text_file_to_github_creates_file(monkeypatch) -> None:
    calls: dict = {}

    def fake_get(*args, **kwargs):
        return _Resp(404)

    def fake_put(url, headers=None, json=None, timeout=None):
        calls["json"] = json
        return _Resp(201, {"content": {"html_url": "https://github.com/o/r/blob/main/a.py"}})

    fake_requests = types.SimpleNamespace(get=fake_get, put=fake_put)
    monkeypatch.setenv("GITHUB_TOKEN", "x")
    monkeypatch.setitem(__import__("sys").modules, "requests", fake_requests)

    url = push_text_file_to_github("o/r", "a.py", "print(1)", "msg")
    assert "github.com" in url
    assert calls["json"]["message"] == "msg"
    decoded = base64.b64decode(calls["json"]["content"]).decode("utf-8")
    assert decoded == "print(1)"
