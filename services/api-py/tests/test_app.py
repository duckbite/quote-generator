import os
import json
from fastapi.testclient import TestClient

os.environ.setdefault("DDB_TABLE_NAME", "quote-generator-prod")

from src.app import app, build_cache_key  # noqa: E402


client = TestClient(app)


def test_build_cache_key_stable():
    a = build_cache_key("ducks", "concise", "short", "gpt-4o-mini")
    b = build_cache_key("Ducks", "concise", "short", "gpt-4o-mini")
    assert a == b


def test_get_quote_works(monkeypatch):
    def fake_generate(topic, style, length):
        return {"quote": "A concise short quote about ducks.", "attribution": None, "source": "generated"}

    # Patch the generator
    from src import app as app_module

    monkeypatch.setattr(app_module, "generate_quote_with_openai", fake_generate)
    monkeypatch.setattr(app_module, "get_cache", lambda pk, sk: None)
    monkeypatch.setattr(app_module, "put_cache", lambda pk, sk, q, a, ttl_seconds: None)

    res = client.get("/quote")
    assert res.status_code == 200
    data = res.json()
    assert "quote" in data and isinstance(data["quote"], str)

