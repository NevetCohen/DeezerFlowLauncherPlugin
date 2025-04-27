# Project Tasks

## Phase 1: Setup & Basic API (from PLANNING.md)

- [ ] Set up Flow Launcher Python plugin boilerplate (Partially done by creating files).
- [ ] Define actual values in `plugin.json` (ID, Author, Website).
- [ ] Implement basic API calls in `deezer_client.py` (Initial structure exists).
- [ ] Verify basic API connectivity (e.g., run `deezer_client.py` directly).
- [ ] Handle potential Deezer API authentication (OAuth or App Key - Investigate necessity).
- [ ] Integrate `DeezerClient` into `main.py`.

## Phase 2: Search Implementation

- [ ] Implement specific search logic (album, artist, playlist) in `deezer_client.py`.
- [ ] Integrate `thefuzz` library for fuzzy matching in `main.py` or `deezer_client.py`.
- [ ] Format search results properly for Flow Launcher in `main.py` (Title, SubTitle, IcoPath, JsonRPCAction).

## Phase 3: Playback Initiation

- [ ] Ensure `JsonRPCAction` in `main.py` correctly calls `open_url` with the correct Deezer URL from `deezer_client.py`.
- [ ] Investigate if direct playback initiation via URL parameters is possible.

## Phase 4: Web Play/Pause Control (Basic)

- [ ] Refine `play`/`stop` command behavior in `main.py` (currently just opens Deezer).

## Phase 5: Testing & Refinement

- [ ] Add unit tests for `deezer_client.py` functions in `tests/test_deezer_client.py`.
- [ ] Refine fuzzy search parameters.
- [ ] Add error handling and user feedback (e.g., API errors, no results found).
- [ ] Add Docstrings and Type Hints throughout.
- [ ] Format code using `black`.
- [ ] Create/find a suitable icon for `Icons/app.png`.

## Discovered During Work

- (Add items here as they come up) 