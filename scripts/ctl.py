"""Tiny desktop control helper: screenshots, mouse, keyboard (Windows, ctypes)."""
import sys, time, ctypes
from ctypes import wintypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()
u = ctypes.windll.user32

def shot(out, x0=0, y0=0, w=1920, h=1200, scale=1.0):
    from PIL import ImageGrab
    im = ImageGrab.grab(bbox=(x0, y0, x0 + w, y0 + h), all_screens=True)
    if scale != 1.0:
        im = im.resize((int(im.width * scale), int(im.height * scale)))
    im.save(out)

def move(x, y, smooth=True, dur=0.6):
    if smooth:
        p = wintypes.POINT(); u.GetCursorPos(ctypes.byref(p))
        n = max(int(dur * 60), 1)
        for i in range(1, n + 1):
            t = i / n; t = t * t * (3 - 2 * t)
            u.SetCursorPos(int(p.x + (x - p.x) * t), int(p.y + (y - p.y) * t)); time.sleep(dur / n)
    u.SetCursorPos(int(x), int(y))

def click(x, y, button="left", double=False):
    move(x, y)
    time.sleep(0.15)
    down, up = (0x2, 0x4) if button == "left" else (0x8, 0x10)
    for _ in range(2 if double else 1):
        u.mouse_event(down, 0, 0, 0, 0); time.sleep(0.05); u.mouse_event(up, 0, 0, 0, 0); time.sleep(0.08)

def scroll(x, y, clicks):
    move(x, y)
    for _ in range(abs(clicks)):
        u.mouse_event(0x800, 0, 0, 120 if clicks > 0 else -120, 0); time.sleep(0.12)

def drag(x1, y1, x2, y2, dur=1.5):
    move(x1, y1); time.sleep(0.1)
    u.mouse_event(0x2, 0, 0, 0, 0); time.sleep(0.1)
    move(x2, y2, dur=dur); time.sleep(0.1)
    u.mouse_event(0x4, 0, 0, 0, 0)

VK = {"ctrl": 0x11, "shift": 0x10, "alt": 0x12, "win": 0x5B, "tab": 0x09, "enter": 0x0D, "esc": 0x1B,
      "del": 0x2E, "home": 0x24, "end": 0x23, "pgdn": 0x22, "pgup": 0x21, "up": 0x26, "down": 0x28,
      "left": 0x25, "right": 0x27, "backspace": 0x08, "f5": 0x74}
def key(combo):
    keys = [VK[k] if k in VK else ord(k.upper()) for k in combo.lower().split("+")]
    for k in keys: u.keybd_event(k, 0, 0, 0); time.sleep(0.03)
    for k in reversed(keys): u.keybd_event(k, 0, 2, 0); time.sleep(0.03)

def typetext(s):
    for ch in s:
        r = u.VkKeyScanW(ord(ch)); vk = r & 0xFF; sh = (r >> 8) & 1
        if sh: u.keybd_event(0x10, 0, 0, 0)
        u.keybd_event(vk, 0, 0, 0); u.keybd_event(vk, 0, 2, 0)
        if sh: u.keybd_event(0x10, 0, 2, 0)
        time.sleep(0.03)

if __name__ == "__main__":
    a = sys.argv[1:]
    cmd = a[0]
    if cmd == "shot":
        shot(a[1], *[int(v) for v in a[2:6]], *( [float(a[6])] if len(a) > 6 else []))
    elif cmd == "click": click(int(a[1]), int(a[2]))
    elif cmd == "dbl": click(int(a[1]), int(a[2]), double=True)
    elif cmd == "rclick": click(int(a[1]), int(a[2]), button="right")
    elif cmd == "move": move(int(a[1]), int(a[2]))
    elif cmd == "scroll": scroll(int(a[1]), int(a[2]), int(a[3]))
    elif cmd == "drag": drag(*[int(v) for v in a[1:5]])
    elif cmd == "key": key(a[1])
    elif cmd == "type": typetext(a[1])
