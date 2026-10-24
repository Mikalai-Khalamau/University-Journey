import pytest
from shared.responses.status import StatusResponse
from shared.responses.success import SuccessResponse
from shared.utils.env import get_env

class TestResponses:
    def test_status_response_to_dict(self):
        resp = StatusResponse(404, "Not found")
        assert resp.to_dict() == {"code": 404, "message": "Not found"}

    def test_success_response_with_model(self):
        class DummyModel:
            def to_dict(self): return {"val": 1}
        resp = SuccessResponse(200, "OK", DummyModel())
        assert resp.to_dict() == {"code": 200, "message": "OK", "data": {"val": 1}}

    def test_success_response_with_dict(self):
        resp = SuccessResponse(200, "OK", {"key": "value"})
        assert resp.to_dict() == {"code": 200, "message": "OK", "data": {"key": "value"}}

class TestUtils:
    def test_get_env_exists(self, monkeypatch):
        monkeypatch.setenv("TEST_VAR", "hello")
        assert get_env("TEST_VAR", "fallback") == "hello"

    def test_get_env_missing(self):
        assert get_env("NON_EXISTENT", "fallback") == "fallback"