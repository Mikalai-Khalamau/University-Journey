from unittest.mock import MagicMock, patch

from insurance.services.http import http_get_json


@patch("insurance.services.http.urllib.request.urlopen")
def test_http_get_json_parses(mock_open):
    resp = MagicMock()
    resp.__enter__.return_value = resp
    resp.__exit__.return_value = False
    resp.read.return_value = b'{"hello": "world"}'
    mock_open.return_value = resp
    assert http_get_json("https://example.com/test") == {"hello": "world"}
