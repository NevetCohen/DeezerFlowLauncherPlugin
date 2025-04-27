# Project Tasks

## Phase 1: Setup & Basic API (from PLANNING.md)

- [x] Set up Flow Launcher Python plugin boilerplate (Partially done by creating files). *(Easy)*
- [x] Define actual values in `plugin.json` (ID, Author, Website). *(Easy)*
- [x] Implement basic API calls in `deezer_client.py` (Initial structure exists). *(Medium)*
- [x] Verify basic API connectivity (e.g., run `deezer_client.py` directly). *(Easy)*
- [x] Investigate Deezer API authentication requirements for `/search` endpoint. *(Medium)*
- [ ] Register an application on the Deezer Developer Portal (if required by investigation). *(Easy) - **Blocked: Deezer not accepting new apps currently.***
- [-] *If OAuth required:* (Blocked by registration)
    - [-] Determine appropriate OAuth flow (e.g., Authorization Code, Client Credentials) for a Flow plugin context. *(Medium)*
    - [-] Implement chosen OAuth flow to obtain an initial access token. *(Medium)*
    - [-] Implement secure storage (e.g., Flow settings) and refresh logic for OAuth tokens. *(Medium)*
- [-] *If App Key/Secret sufficient:* (Blocked by registration)
    - [-] Implement passing App Key/Secret with API requests in `deezer_client.py`. *(Easy)*
    - [-] Implement secure way to store/retrieve App Key/Secret (e.g., Flow settings). *(Easy)*
- [x] Integrate `DeezerClient` into `main.py`. *(Medium)*
- [-] Create GitHub repository and provide URL. *(Manual - User)* (Deferred - Let's finish core logic first)
- [-] Push initial commit and 'PLAN' tag to remote GitHub repository. *(Easy)* (Deferred - Depends on repo creation)

## Phase 2: Search Implementation

- [x] Implement specific search logic (album, artist, playlist) in `deezer_client.py`. *(Medium)*
- [x] Integrate `thefuzz` library for fuzzy matching in `main.py` or `deezer_client.py`. *(Medium)*
- [x] Format search results properly for Flow Launcher in `main.py` (Title, SubTitle, IcoPath, JsonRPCAction). *(Medium)*

## Phase 3: Playback Initiation

- [-] ~~Ensure `JsonRPCAction` in `main.py` correctly calls `open_url` with the correct Deezer URL from `deezer_client.py`. *(Easy)*~~ (Superseded by Desktop App strategy)
- [-] ~~Investigate if direct playback initiation via URL parameters is possible. *(Medium)*~~ (Superseded by Desktop App strategy)

## Phase 3 (New): Desktop App Generic Control

- [ ] Investigate feasibility and method for simulating OS media key presses (Play/Pause, Stop) using Python (e.g., with `pynput`). *(Medium)*
- [ ] Add chosen library (e.g., `pynput`) to `requirements.txt`. *(Easy)*
- [ ] Implement functions in `main.py` or a helper module to send Play/Pause and Stop media key signals. *(Medium)*
- [ ] Modify `main.py` query logic to call the media key functions for `de play` (no search term), `de stop`, `de pause` commands. *(Medium)*
- [ ] Update Flow results for these commands to indicate they target the Desktop App. *(Easy)*

## Phase 4: Desktop App Specific Content Control

- [ ] **Investigate:** Research Deezer Desktop App's custom URI scheme or command-line arguments for playing specific content IDs (albums, tracks, etc.). *(High)*
- [ ] **Implement:** If a method is found:
    - [ ] Extract necessary IDs (album, track, etc.) from API results in `main.py` or `deezer_client.py`. *(Medium)*
    - [ ] Construct the appropriate URI or command line in `main.py`. *(Medium)*
    - [ ] Implement calling the URI/command (e.g., `os.startfile`, `subprocess.run`) in `main.py`. *(Medium)*
    - [ ] Update Flow results for `play <item>` to use the new desktop action. *(Medium)*
- [ ] **Fallback:** Implement fallback behavior (e.g., focus app) if specific playback cannot be triggered. *(Easy)*

## Phase 5: Testing & Refinement

- [x] Add unit tests for `deezer_client.py` functions in `tests/test_deezer_client.py`. *(Medium)*
- [ ] Refine fuzzy search parameters. *(Medium)*
- [ ] Add error handling and user feedback (e.g., API errors, no results found). *(Medium)*
- [ ] Add Docstrings and Type Hints throughout. *(Easy)*
- [ ] Format code using `black`. *(Easy)*
- [ ] Create/find a suitable icon for `Icons/app.png`. *(Easy)*

## Discovered During Work

- (Add items here as they come up) 