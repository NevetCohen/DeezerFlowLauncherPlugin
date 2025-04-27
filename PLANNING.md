# PLANNING.md

## Project Goal

To create a Flow Launcher plugin that allows users to quickly search Deezer and control playback **exclusively within the Deezer Desktop App** using the shortcut `de`.

## Core Features

- **Shortcut Activation:** Trigger plugin using `de`.
- **Commands:**
    - `play`: Attempt to send an OS-level 'Play/Pause' media key command, targeting the Deezer Desktop App (if running).
    - `stop`/`pause`: Attempt to send an OS-level 'Play/Pause' or 'Stop' media key command, targeting the Deezer Desktop App (if running).
    - `play <album name>`: Search Deezer via API and attempt to trigger playback of the best match **in the Desktop App**.
    - `play <artist name>`: Search Deezer via API and attempt to trigger playback of the artist's top tracks **in the Desktop App**.
    - `play <playlist name>`: Search Deezer via API and attempt to trigger playback of the best match **in the Desktop App**.
    - `play <track name>`: Search Deezer via API and attempt to trigger playback of the best match **in the Desktop App**.
- **Fuzzy Search:** Handle typos and variations in search queries for albums, artists, playlists, and tracks.
- **Feedback:** Display search results (indicating they will target the desktop app) and actions within Flow Launcher.

## Architecture

- **Plugin Structure:** Standard Flow Launcher Python plugin structure (`plugin.json`, main Python script).
- **Deezer Interaction:**
    - Use the official Deezer API (`api.deezer.com`) for searching albums, artists, playlists, and tracks to get IDs and metadata.
    - **Authentication:**
        - **Current Status (Important):** As of [Date - e.g., Aug 2024], Deezer is **not accepting new application registrations**. Basic API search works without authentication.
        - **Future Needs:** Unlikely to be needed unless Deezer adds desktop app control features requiring OAuth, which is currently blocked anyway.
    - **Desktop App Control:**
        - **Generic Controls (`play`/`stop`/`pause`):** The primary approach will be to **simulate OS-level media key presses** (Play/Pause, Stop). This relies on the Deezer Desktop App being installed, running, and responsive to these keys.
        - **Specific Content Playback (`play <item>`):** This is the main challenge. Requires investigation into:
            - **Custom URI Scheme:** Does the Deezer Desktop App register a scheme like `deezer://play?type=album&id={id}` that can be called by the OS?
            - **Command-Line Arguments:** Can `Deezer.exe` be launched with arguments specifying content to play?
            - **Other IPC/Automation:** Less likely methods like OS-level automation or inter-process communication.
        - **Fallback:** If triggering specific content fails, the `play <item>` commands might fall back to just bringing the Deezer Desktop App to the foreground.
        - **Web Player control is explicitly out of scope.**
- **Search Logic:** Implement fuzzy matching using a library like `thefuzz` to improve search tolerance.
- **UI:** Utilize Flow Launcher's result list API to display search results and actions targeting the desktop app.

## Key Technologies

- **Language:** Python 3.x
- **Framework:** Flow Launcher Plugin API
- **Libraries:**
    - `requests`: For interacting with the Deezer API.
    - `thefuzz` (or similar like `fuzzywuzzy`): For fuzzy string matching.
    - `pynput` (Potential): For simulating OS-level keyboard events (like media keys).
    - `subprocess` / `os` (Potential): For launching Deezer with arguments or opening URI schemes.
    - ~~`webbrowser`~~ (Removed: No longer opening web URLs).
    - ~~Potentially a library for handling OAuth flow if needed for API authentication.~~ (Deferred due to registration block)
    - `pydantic` (Optional): For structuring API responses or plugin settings.

## Development Plan / Phases

1.  **Setup & Basic API:** (Mostly Complete)
    - Set up Flow Launcher Python plugin boilerplate.
    - Implement basic API calls (search) and verify connectivity.
    - Define `plugin.json`.
2.  **Search Implementation:** (Mostly Complete)
    - Implement search logic for albums, artists, playlists, tracks using the Deezer API.
    - Integrate fuzzy search library.
    - Display search results in Flow Launcher (update text to reflect desktop target).
3.  **Desktop App Generic Control:**
    - Investigate and implement simulating OS media key presses (Play/Pause, Stop) using `pynput` or similar.
    - Add logic in `main.py` to trigger these keys for `de play` (no search term), `de stop`, `de pause`.
    - Update Flow results for these commands.
4.  **Desktop App Specific Content Control:**
    - **Investigate:** Research Deezer Desktop App's custom URI scheme or command-line arguments for playing specific content IDs (albums, tracks, etc.).
    - **Implement:** If a method is found, modify `main.py` / `deezer_client.py`:
        - Extract necessary IDs (album, track, etc.) from API results.
        - Construct the appropriate URI or command line.
        - Use `os.startfile` (for URIs) or `subprocess.run` (for commands) to trigger playback in the desktop app for `play <item>` results.
    - **Fallback:** Implement fallback behavior (e.g., just focus app) if specific playback cannot be triggered.
5.  **Testing & Refinement:**
    - Add/update unit tests for API logic.
    - Test media key simulation reliability.
    - Test specific content triggering reliability.
    - Refine fuzzy search parameters.
    - Improve error handling and user feedback.
    - Add docstrings and type hints.
    - Format code using `black`.

## Potential Challenges

- **Desktop App Specific Content Control:** Finding a reliable way (URI scheme, command-line) to trigger specific content playback in the Deezer Desktop App is the main uncertainty. This might not be possible.
- **Desktop App Control Reliability (Generic Keys):** Simulating media keys might not work if the Deezer Desktop App isn't running, isn't the active media application, or doesn't respond correctly. Requires desktop app installation.
- **API Authentication:** (Currently Blocked) Less relevant now, as desktop control likely doesn't use the API auth, but registration block still exists.
- **API Rate Limits:** Still applies to API searches.
- **Fuzzy Search Accuracy:** Still applies.
- **Platform Differences:** Media key simulation and URI/command-line launching might differ across OS versions.

## Style & Conventions

- Follow **PEP8** guidelines strictly.
- Use **Type Hints** for all function signatures and critical variables.
- Format code using **`black`**.
- Write **Google Style Docstrings** for all classes, methods, and functions.
- Structure code modularly.
- Keep files under 500 lines; refactor if necessary.
- Add unit tests to a `/tests` directory mirroring the main structure.
