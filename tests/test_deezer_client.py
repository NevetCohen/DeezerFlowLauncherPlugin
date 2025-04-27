import pytest
import requests
from unittest.mock import MagicMock  # Use unittest.mock if pytest-mock isn't explicitly installed or preferred

# Assuming deezer_client.py is in the parent directory relative to tests/
# Adjust the import path if your structure is different
from deezer_client import DeezerClient, DEEZER_API_BASE

# --- Fixtures ---

@pytest.fixture
def client() -> DeezerClient:
    """Provides a DeezerClient instance for tests."""
    return DeezerClient()

@pytest.fixture
def mock_session_get(mocker):
    """Mocks the requests.Session.get method."""
    return mocker.patch('requests.Session.get')

# --- Test Cases ---

def test_client_init_no_token():
    """Test client initialization without an access token."""
    client_instance = DeezerClient()
    assert client_instance.access_token is None
    assert "Authorization" not in client_instance.session.headers

def test_client_init_with_token():
    """Test client initialization with an access token."""
    token = "test_token_123"
    client_instance = DeezerClient(access_token=token)
    assert client_instance.access_token == token
    assert "Authorization" in client_instance.session.headers
    assert client_instance.session.headers["Authorization"] == f"Bearer {token}"

def test_make_request_success(client, mock_session_get):
    """Test _make_request handles a successful API call."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": [{"id": 1, "title": "Test"}]}
    mock_response.raise_for_status.return_value = None  # Simulate successful status
    mock_session_get.return_value = mock_response

    endpoint = "/search/track"
    params = {"q": "test"}
    result = client._make_request(endpoint, params=params)

    expected_url = f"{DEEZER_API_BASE}{endpoint}"
    mock_session_get.assert_called_once_with(expected_url, params=params)
    assert result == {"data": [{"id": 1, "title": "Test"}]}

def test_make_request_http_error(client, mock_session_get):
    """Test _make_request handles an HTTP error (e.g., 404, 500)."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
    mock_session_get.return_value = mock_response

    endpoint = "/invalid/endpoint"
    with pytest.raises(requests.exceptions.HTTPError):
        client._make_request(endpoint)

def test_make_request_deezer_api_error(client, mock_session_get):
    """Test _make_request handles a Deezer-specific API error in the JSON response."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"error": {"type": "OAuthException", "message": "Invalid token"}}
    mock_response.raise_for_status.return_value = None
    mock_session_get.return_value = mock_response

    endpoint = "/search/track"
    with pytest.raises(ValueError, match="Deezer API Error: Invalid token \(Type: OAuthException\)"):
        client._make_request(endpoint)

def test_search_calls_make_request(client, mocker):
    """Test that the search method calls _make_request with correct parameters."""
    mock_make_request = mocker.patch.object(client, '_make_request', return_value={"data": [{"id": 1}]})
    query = "test query"
    search_type = "album"

    results = client.search(query, search_type=search_type)

    expected_endpoint = f"/search/{search_type}"
    expected_params = {"q": query}
    mock_make_request.assert_called_once_with(expected_endpoint, params=expected_params)
    assert results == [{"id": 1}]

def test_search_invalid_type_uses_general_search(client, mocker):
    """Test search falls back to general /search if type is invalid."""
    mock_make_request = mocker.patch.object(client, '_make_request', return_value={"data": []})
    query = "test query"
    search_type = "invalid_type"

    client.search(query, search_type=search_type)

    expected_endpoint = "/search"
    expected_params = {"q": query}
    mock_make_request.assert_called_once_with(expected_endpoint, params=expected_params)

def test_search_handles_request_error(client, mocker):
    """Test search returns empty list if _make_request raises an error."""
    mocker.patch.object(client, '_make_request', side_effect=requests.exceptions.RequestException)
    results = client.search("test", "track")
    assert results == []

def test_search_albums_calls_search(client, mocker):
    """Test search_albums calls search with type 'album'."""
    mock_search = mocker.patch.object(client, 'search', return_value=[])
    query = "test album"
    client.search_albums(query)
    mock_search.assert_called_once_with(query, search_type="album")

def test_search_artists_calls_search(client, mocker):
    """Test search_artists calls search with type 'artist'."""
    mock_search = mocker.patch.object(client, 'search', return_value=[])
    query = "test artist"
    client.search_artists(query)
    mock_search.assert_called_once_with(query, search_type="artist")

def test_search_playlists_calls_search(client, mocker):
    """Test search_playlists calls search with type 'playlist'."""
    mock_search = mocker.patch.object(client, 'search', return_value=[])
    query = "test playlist"
    client.search_playlists(query)
    mock_search.assert_called_once_with(query, search_type="playlist")

def test_get_item_url_success(client):
    """Test get_item_url extracts the link correctly."""
    item = {"id": 1, "title": "Test", "link": "https://deezer.com/track/1"}
    assert client.get_item_url(item) == "https://deezer.com/track/1"

def test_get_item_url_no_link(client):
    """Test get_item_url returns None if 'link' key is missing."""
    item = {"id": 1, "title": "Test"}
    assert client.get_item_url(item) is None

def test_get_item_url_empty_dict(client):
    """Test get_item_url returns None for an empty dictionary."""
    item = {}
    assert client.get_item_url(item) is None 