# -*- coding: utf-8 -*-
import sys
import os
import webbrowser
from typing import List, Dict, Any # Added typing imports
from flowlauncher import FlowLauncher, FlowLauncherAPI
from thefuzz import fuzz

# Ensure the plugin directory is in the path for local imports
plugin_dir = os.path.dirname(__file__)
if plugin_dir not in sys.path:
    sys.path.append(plugin_dir)

from deezer_client import DeezerClient # Import the client
from media_keys import send_play_pause, send_stop  # Import media key functions

# TODO: Potentially import fuzzy search library

class DeezerControl(FlowLauncher):
    """Flow Launcher plugin to interact with Deezer."""

    # Define constant for max results per type
    MAX_RESULTS_PER_TYPE = 3

    def __init__(self):
        """Initialize the plugin and Deezer client."""
        # Initialize DeezerClient *before* calling super init
        # to ensure it exists if super init calls query
        self.deezer = DeezerClient()
        super().__init__()
        # Initialize DeezerClient (no auth token needed for basic search)
        # self.deezer = DeezerClient()

    def _format_result(self, item: Dict[str, Any], item_type: str) -> Dict[str, Any]:
        """Helper function to format a Deezer item for Flow Launcher."""
        result = {
            "Title": "Unknown Item",
            "SubTitle": f"Type: {item_type}",
            "IcoPath": "Icons\\app.png", # Use default icon for now
            "JsonRPCAction": {}
        }
        url = self.deezer.get_item_url(item)

        if item_type == "artist":
            result["Title"] = item.get("name", "Unknown Artist")
            result["SubTitle"] = "Artist"
        elif item_type == "album":
            artist_name = item.get('artist', {}).get('name', 'Unknown Artist')
            result["Title"] = f"{item.get('title', 'Unknown Album')} by {artist_name}"
            result["SubTitle"] = "Album"
        elif item_type == "playlist":
            creator_name = item.get('user', {}).get('name', 'Unknown Creator')
            result["Title"] = f"{item.get('title', 'Unknown Playlist')} by {creator_name}"
            result["SubTitle"] = "Playlist"
        elif item_type == "track":
            artist_name = item.get('artist', {}).get('name', 'Unknown Artist')
            album_title = item.get('album', {}).get('title', 'Unknown Album')
            result["Title"] = f"{item.get('title', 'Unknown Track')} by {artist_name}"
            result["SubTitle"] = f"Track from {album_title}"

        if url:
            result["JsonRPCAction"] = {
                "method": "open_url",
                "parameters": [url]
            }
        else:
            # Disable action if no URL found
            result["SubTitle"] += " (No URL found)"

        return result

    def _fuzzy_sort(self, items: List[Dict[str, Any]], search_term: str, item_type: str) -> List[Dict[str, Any]]:
        """Sorts items by fuzzy similarity to the search term."""
        def get_compare_string(item: Dict[str, Any]) -> str:
            if item_type == "artist":
                return item.get("name", "")
            elif item_type == "album":
                return item.get("title", "") + " " + item.get("artist", {}).get("name", "")
            elif item_type == "playlist":
                return item.get("title", "") + " " + item.get("user", {}).get("name", "")
            elif item_type == "track":
                return item.get("title", "") + " " + item.get("artist", {}).get("name", "")
            return ""
        # Score and sort
        scored = [
            (item, fuzz.token_set_ratio(search_term.lower(), get_compare_string(item).lower()))
            for item in items
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [item for item, score in scored]

    def query(self, query: str) -> list:
        """Handle user queries from Flow Launcher."""
        results = []
        query = query.strip() # Clean query

        if not query:
            # Initial state or empty query
            results.append({
                "Title": "Deezer Control: Type 'play <search>', 'artist <search>', 'album <search>', 'playlist <search>'",
                "SubTitle": "Example: play master of puppets OR artist metallica",
                "IcoPath": "Icons\\app.png"
            })
            return results

        parts = query.lower().split(' ', 1)
        command = parts[0]
        search_term = parts[1] if len(parts) > 1 else ""

        # Determine search type based on command, default to track
        search_types_to_run = []
        if command == "play":
             if not search_term:
                 # Simple 'play' command - send Play/Pause media key
                 results.append({
                     "Title": "Play/Pause Deezer Desktop App",
                     "SubTitle": "Sends Play/Pause media key to the Deezer Desktop App (must be running)",
                     "IcoPath": "Icons\\app.png",
                     "JsonRPCAction": {
                         "method": "play_pause_desktop",
                         "parameters": []
                     }
                 })
                 return results
             else:
                 # 'play <term>' searches tracks primarily
                 search_types_to_run = ["track", "album", "artist"] # Prioritize tracks
        elif command == "artist":
            if search_term: search_types_to_run = ["artist"]
        elif command == "album":
            if search_term: search_types_to_run = ["album"]
        elif command == "playlist":
            if search_term: search_types_to_run = ["playlist"]
        elif command == "stop":
             results.append({
                    "Title": "Stop Deezer Desktop App",
                    "SubTitle": "Sends Stop media key to the Deezer Desktop App (must be running)",
                    "IcoPath": "Icons\\app.png",
                    "JsonRPCAction": {
                        "method": "stop_desktop",
                        "parameters": []
                    }
                })
             return results
        elif command == "pause":
             results.append({
                    "Title": "Pause Deezer Desktop App",
                    "SubTitle": "Sends Play/Pause media key to the Deezer Desktop App (must be running)",
                    "IcoPath": "Icons\\app.png",
                    "JsonRPCAction": {
                        "method": "play_pause_desktop",
                        "parameters": []
                    }
                })
             return results
        else:
            # No specific command, assume general search (treat whole query as search term)
            search_term = query
            search_types_to_run = ["track", "artist", "album", "playlist"]

        if not search_term:
            results.append({
                "Title": f"Please provide a search term after '{command}'.",
                "IcoPath": "Icons\\app.png"
                })
            return results

        # Perform searches
        # TODO: Consider running searches concurrently if performance is an issue
        found_items = []
        if "artist" in search_types_to_run:
            artists = self.deezer.search_artists(search_term)
            artists = self._fuzzy_sort(artists, search_term, "artist")
            found_items.extend([(item, "artist") for item in artists[:self.MAX_RESULTS_PER_TYPE]])
        if "album" in search_types_to_run:
            albums = self.deezer.search_albums(search_term)
            albums = self._fuzzy_sort(albums, search_term, "album")
            found_items.extend([(item, "album") for item in albums[:self.MAX_RESULTS_PER_TYPE]])
        if "playlist" in search_types_to_run:
            playlists = self.deezer.search_playlists(search_term)
            playlists = self._fuzzy_sort(playlists, search_term, "playlist")
            found_items.extend([(item, "playlist") for item in playlists[:self.MAX_RESULTS_PER_TYPE]])
        if "track" in search_types_to_run:
            tracks = self.deezer.search(search_term, search_type="track")
            tracks = self._fuzzy_sort(tracks, search_term, "track")
            found_items.extend([(item, "track") for item in tracks[:self.MAX_RESULTS_PER_TYPE]])

        # Format results
        if found_items:
            for item, item_type in found_items:
                 results.append(self._format_result(item, item_type))
        else:
            results.append({
                "Title": f"No Deezer results found for '{search_term}'",
                "SubTitle": f"Searched types: {', '.join(search_types_to_run)}",
                "IcoPath": "Icons\\app.png"
            })

        return results

    def open_url(self, url: str):
        """Opens the specified URL in the default web browser."""
        webbrowser.open(url)
        # Optional: Show brief confirmation (can be annoying)
        # FlowLauncherAPI.show_msg("Opening Deezer", f"Navigating to {url}")

    # Add RPC methods for FlowLauncher to call
    def play_pause_desktop(self):
        """Send Play/Pause media key to the OS (Deezer Desktop App)."""
        send_play_pause()

    def stop_desktop(self):
        """Send Stop media key to the OS (Deezer Desktop App)."""
        send_stop()

if __name__ == "__main__":
    DeezerControl() 