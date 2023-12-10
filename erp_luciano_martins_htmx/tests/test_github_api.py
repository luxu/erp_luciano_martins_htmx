from unittest.mock import Mock

import pytest

from core import github_api

@pytest.fixture
def avatar_url():
    resp_mock = Mock()
    url = "https://avatars.githubusercontent.com/u/1096573?v=4"
    resp_mock.json.return_value = {
        "login": "luxu",
        "id": 1096573,
        "avatar_url": url,
    }
    get_original = github_api.get
    github_api.get = Mock(return_value=resp_mock)
    yield url
    github_api.get = get_original


def test_buscar_avatar(avatar_url):
    url = github_api.buscar_avatar("luxu")
    assert avatar_url == url


def test_buscar_avatar_integracao():
    url = github_api.buscar_avatar("luxu")
    assert "https://avatars.githubusercontent.com/u/1096573?v=4" == url
