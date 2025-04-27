from pynput.keyboard import Controller, Key, KeyCode


def send_play_pause() -> None:
    """Send the Play/Pause media key signal to the OS.

    This function simulates pressing the Play/Pause media key, which should
    control playback in the active media application (e.g., Deezer Desktop App).

    Returns:
        None
    """
    keyboard = Controller()
    try:
        # Use Key.media_play_pause if available, else fallback to virtual key code
        try:
            keyboard.press(Key.media_play_pause)
            keyboard.release(Key.media_play_pause)
        except AttributeError:
            # Fallback for older pynput versions
            keyboard.press(KeyCode.from_vk(0xB3))  # Play/Pause
            keyboard.release(KeyCode.from_vk(0xB3))
    except Exception as e:
        # Optionally log or handle errors
        pass


def send_stop() -> None:
    """Send the Stop media key signal to the OS.

    This function simulates pressing the Stop media key, which should
    stop playback in the active media application (if supported).

    Returns:
        None
    """
    keyboard = Controller()
    try:
        keyboard.press(KeyCode.from_vk(0xB2))  # Stop
        keyboard.release(KeyCode.from_vk(0xB2))
    except Exception as e:
        # Optionally log or handle errors
        pass 