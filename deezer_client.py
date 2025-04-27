# -*- coding: utf-8 -*-
from typing import List, Dict, Any, Optional
import requests

# TODO: Add fuzzy search library import if used here

# TODO: Add Pydantic models for API responses if desired

DEEZER_API_BASE = "https://api.deezer.com"

class DeezerClient:
    """A client to interact with the Deezer API."""

    def __init__(self, access_token: Optional[str] = None):
        """Initialize the client.

        Args:
            access_token: Optional OAuth access token for authenticated requests.
        """
        self.access_token = access_token
        self.session = requests.Session()
        if self.access_token:
            self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})
        # TODO: Implement proper OAuth handling/refresh logic if needed

    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Makes a GET request to the Deezer API.

        Args:
            endpoint: The API endpoint path (e.g., '/search/album').
            params: Optional dictionary of query parameters.

        Returns:
            The JSON response from the API as a dictionary.

        Raises:
            requests.exceptions.RequestException: If the request fails.
            ValueError: If the API returns an error.
        """
        url = f"{DEEZER_API_BASE}{endpoint}"
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            if 'error' in data:
                # Deezer API specific error handling
                raise ValueError(f"Deezer API Error: {data['error'].get('message', 'Unknown error')} (Type: {data['error'].get('type')})")
            return data
        except requests.exceptions.RequestException as e:
            # Log error or handle specific exceptions
            print(f"Error making request to {url}: {e}")
            raise

    def search(self, query: str, search_type: str = "track") -> List[Dict[str, Any]]:
        """Performs a general search on Deezer.

        Args:
            query: The search term.
            search_type: Type of search (track, album, artist, playlist). Defaults to track.

        Returns:
            A list of search result items (dictionaries).
        """
        # Basic search - might need refinement for specific types
        endpoint = f"/search"
        params = {"q": query}
        # TODO: Potentially specify type if API supports e.g., /search/{type}?q=...
        # endpoint = f"/search/{search_type}"

        try:
            results = self._make_request(endpoint, params=params)
            return results.get("data", [])
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Error searching Deezer for '{query}': {e}")
            return []

    def search_albums(self, query: str) -> List[Dict[str, Any]]:
        """Searches specifically for albums.

        Args:
            query: The album name to search for.

        Returns:
            A list of album result items.
        """
        # Placeholder - uses general search for now
        # TODO: Refine if /search/album endpoint behaves differently or provides more useful data
        return self.search(query, search_type="album")

    def search_artists(self, query: str) -> List[Dict[str, Any]]:
        """Searches specifically for artists.

        Args:
            query: The artist name to search for.

        Returns:
            A list of artist result items.
        """
        # Placeholder - uses general search for now
        return self.search(query, search_type="artist")

    def search_playlists(self, query: str) -> List[Dict[str, Any]]:
        """Searches specifically for playlists.

        Args:
            query: The playlist name to search for.

        Returns:
            A list of playlist result items.
        """
        # Placeholder - uses general search for now
        return self.search(query, search_type="playlist")

    def get_item_url(self, item: Dict[str, Any]) -> Optional[str]:
        """Extracts the web URL from a Deezer API item.

        Args:
            item: A dictionary representing a track, album, artist, or playlist from the API.

        Returns:
            The web URL string, or None if not found.
        """
        # Common key for web links in Deezer API responses
        return item.get("link")

# Example Usage (for testing)
if __name__ == '__main__':
    client = DeezerClient()
    search_query = "metallica master of puppets"
    print(f"Searching for: {search_query}")
    tracks = client.search(search_query, "track")
    if tracks:
        print("\n--- Tracks ---")
        for track in tracks[:3]: # Show first 3
            print(f"  - {track.get('title')} by {track.get('artist', {}).get('name')} ({client.get_item_url(track)})")

    albums = client.search_albums("master of puppets")
    if albums:
        print("\n--- Albums ---")
        for album in albums[:3]:
            print(f"  - {album.get('title')} by {album.get('artist', {}).get('name')} ({client.get_item_url(album)})") 