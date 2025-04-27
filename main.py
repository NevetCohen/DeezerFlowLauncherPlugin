# -*- coding: utf-8 -*-
import webbrowser
from flowlauncher import FlowLauncher, FlowLauncherAPI

# TODO: Import deezer_client
# from deezer_client import DeezerClient

# TODO: Potentially import fuzzy search library

class DeezerControl(FlowLauncher):
    """Flow Launcher plugin to interact with Deezer."""

    def __init__(self):
        """Initialize the plugin and Deezer client."""
        super().__init__()
        # TODO: Initialize DeezerClient, handle potential auth
        # self.deezer = DeezerClient()

    def query(self, query: str) -> list:
        """Handle user queries from Flow Launcher."""
        results = [] 
        # Placeholder: Parse query, call deezer_client, format results

        if not query:
            # Initial state or empty query
            results.append({
                "Title": "Deezer Control: Type 'play', 'stop', or 'play <search term>'",
                "SubTitle": "Example: play metallica or play master of puppets",
                "IcoPath": "Icons\\app.png"
            })
            return results

        parts = query.lower().strip().split(' ', 1)
        command = parts[0]
        search_term = parts[1] if len(parts) > 1 else ""

        if command == "play":
            if not search_term:
                # Simple 'play' command - potentially open Deezer
                results.append({
                    "Title": "Open Deezer",
                    "SubTitle": "Opens deezer.com in your browser",
                    "IcoPath": "Icons\\app.png",
                    "JsonRPCAction": {
                        "method": "open_url",
                        "parameters": ["https://www.deezer.com"]
                    }
                })
            else:
                # Search and play command
                # TODO: Call DeezerClient search methods (album, artist, playlist)
                # TODO: Use fuzzy matching?
                # TODO: Format search results for Flow Launcher
                # Example placeholder result:
                results.append({
                    "Title": f"Search and Play: {search_term} (Placeholder)",
                    "SubTitle": "Action: Open Deezer search results (Placeholder)",
                    "IcoPath": "Icons\\app.png",
                    "JsonRPCAction": {
                        "method": "open_url",
                        # TODO: Construct actual Deezer search URL or specific item URL
                        "parameters": [f"https://www.deezer.com/search/{search_term}"]
                    }
                })

        elif command in ["stop", "pause"]:
             # Simple 'stop' command - potentially open Deezer
             # TODO: Enhance this? Maybe focus existing tab?
             results.append({
                    "Title": "Open Deezer (for Stop/Pause)",
                    "SubTitle": "Opens deezer.com; manual control required.",
                    "IcoPath": "Icons\\app.png",
                    "JsonRPCAction": {
                        "method": "open_url",
                        "parameters": ["https://www.deezer.com"]
                    }
                })
        else:
            # Unknown command or just search term
            results.append({
                "Title": f"Search Deezer for: {query} (Placeholder)",
                "SubTitle": "Action: Open Deezer search results (Placeholder)",
                "IcoPath": "Icons\\app.png",
                "JsonRPCAction": {
                    "method": "open_url",
                    "parameters": [f"https://www.deezer.com/search/{query}"]
                }
            })

        return results

    def open_url(self, url: str):
        """Opens the specified URL in the default web browser."""
        webbrowser.open(url)
        FlowLauncherAPI.show_msg("Opening Deezer", f"Navigating to {url}")


if __name__ == "__main__":
    DeezerControl() 