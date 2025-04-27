# PLANNING.md

## Project Goal

To create a Flow Launcher plugin that allows users to quickly search for and control music playback on Deezer using the shortcut `de`.

## Core Features

- **Shortcut Activation:** Trigger plugin using `de`.
- **Commands:**
    - `play`: Resume playback in the active Deezer web player tab (Potentially via Javascript SDK interaction or browser extension mechanisms if feasible, otherwise might just open Deezer).
    - `stop`/`pause`: Pause playback in the active Deezer web player tab (Similar approach to `play`).
    - `play <album name>`: Search Deezer for the album and open it in the browser, potentially starting playback.
    - `play <artist name>`: Search Deezer for the artist, open their page or top tracks in the browser, potentially starting playback.
    - `play <playlist name>`: Search Deezer for the playlist and open it in the browser, potentially starting playback.
- **Fuzzy Search:** Handle typos and variations in search queries for albums, artists, and playlists.
- **Feedback:** Display search results and playback status information within Flow Launcher.

## Architecture

- **Plugin Structure:** Standard Flow Launcher Python plugin structure (`plugin.json`, main Python script).
- **Deezer Interaction:**
    - Use the official Deezer API (`api.deezer.com`) for searching albums, artists, and playlists.
    - Authentication (OAuth) will likely be required for API interaction (especially search and potential SDK use). Store credentials securely.
    - **Playback Control & Interaction:**
        - For `play`/`stop`/`pause` commands targeting the *active Deezer tab*, the simplest approach is likely just opening/focusing `deezer.com`. More advanced control might require:
            - Investigating the Deezer Javascript SDK within a browser context (potentially complex to orchestrate from Flow Launcher).
            - Browser extensions or automation tools (likely outside the scope of a simple plugin).
        - For `play <item>` commands, use the API to search. The primary action will be opening the corresponding Deezer web URL (e.g., `https://deezer.com/album/...`). Starting playback automatically might be possible via specific URL parameters or SDK calls if feasible.
- **Search Logic:** Implement fuzzy matching using a library like `thefuzz` to improve search tolerance.
- **UI:** Utilize Flow Launcher's result list API to display search results and actions.

## Key Technologies

- **Language:** Python 3.x
- **Framework:** Flow Launcher Plugin API
- **Libraries:**
    - `requests`: For interacting with the Deezer API.
    - `thefuzz` (or similar like `fuzzywuzzy`): For fuzzy string matching.
    - `webbrowser`: Standard Python library to open URLs in the default browser.
    - Potentially a library for handling OAuth flow if needed for API authentication.
    - `pydantic` (Optional): For structuring API responses or plugin settings.

## Development Plan / Phases

1.  **Setup & Basic API:**
    - Set up Flow Launcher Python plugin boilerplate.
    - Implement basic API calls (e.g., simple search) to verify connectivity and authentication flow (if required).
    - Define `plugin.json`.
2.  **Search Implementation:**
    - Implement search logic for albums, artists, and playlists using the Deezer API.
    - Integrate fuzzy search library.
    - Display search results in Flow Launcher.
3.  **Playback Initiation:**
    - Implement opening Deezer web URLs based on search results using the `webbrowser` module.
    - Investigate if direct playback initiation via URL parameters or simple SDK calls is possible/practical.
    - Handle potential authentication requirements for API search/SDK use.
4.  **Web Play/Pause Control (Basic):**
    - Implement `play`/`stop` commands to simply open `deezer.com` or potentially focus an existing Deezer tab if Flow Launcher/OS allows. Advanced control (actual pause/resume) is a stretch goal depending on complexity.
5.  **Testing & Refinement:**
    - Add basic unit tests (using `pytest`) for API interaction logic and search functionality (place in `/tests`).
    - Refine fuzzy search parameters.
    - Improve error handling and user feedback.
    - Add docstrings and type hints.
    - Format code using `black`.

## Potential Challenges

- **Direct Web Player Control:** Controlling playback (play/pause/next/prev) in an *existing* browser tab from an external application like Flow Launcher is non-trivial and might require browser extensions or complex Javascript injection, potentially limiting functionality to just *opening* URLs.
- **API Authentication:** Implementing and managing OAuth securely within a Flow Launcher plugin.
- **API Rate Limits:** Handling potential rate limits from the Deezer API.
- **Fuzzy Search Accuracy:** Tuning fuzzy search to provide relevant results without being too broad.
- **Identifying Active Tab:** Reliably identifying and interacting with the correct Deezer tab among potentially many browser tabs.
- **Platform Differences:** Removed, as OS-level media keys are no longer the primary approach.

## Style & Conventions

- Follow **PEP8** guidelines strictly.
- Use **Type Hints** for all function signatures and critical variables.
- Format code using **`black`**.
- Write **Google Style Docstrings** for all classes, methods, and functions.
- Structure code modularly, potentially separating Deezer API logic into its own module.
- Keep files under 500 lines; refactor if necessary.
- Add unit tests to a `/tests` directory mirroring the main structure.
