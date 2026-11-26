import sys, time, subprocess, os, imageio_ffmpeg
sys.path.insert(0, os.path.dirname(__file__))
import ctl
FF = imageio_ffmpeg.get_ffmpeg_exe()
OUT = os.path.join(os.path.dirname(__file__), "segs"); os.makedirs(OUT, exist_ok=True)
W = time.sleep
TAB_MAKE, TAB_SHEET, TAB_FINAL = (120, 18), (370, 18), (600, 18)

def record(name, dur, actions):
    out = os.path.join(OUT, name + ".mp4")
    p = subprocess.Popen([FF, "-y", "-hide_banner", "-loglevel", "error", "-f", "gdigrab", "-framerate", "15",
                          "-offset_x", "0", "-offset_y", "0", "-video_size", "1920x1200", "-draw_mouse", "1",
                          "-i", "desktop", "-t", str(dur), "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
                          "-pix_fmt", "yuv420p", out])
    W(0.8)
    actions()
    p.wait()
    print(name, "done", out)

def seg_A():
    W(3); ctl.move(203, 620, dur=1.0); W(1); ctl.move(1793, 620, dur=10); W(1); ctl.move(960, 850, dur=1.5)

def seg_B():
    W(1); ctl.move(203, 620); W(3.5); ctl.move(310, 620); W(3.5)
    ctl.click(415, 620); W(8); ctl.click(782, 1112); W(1.2)
    ctl.click(522, 620); W(7); ctl.click(888, 1013); W(1)

def seg_C1():
    ctl.click(*TAB_SHEET); W(1); ctl.move(530, 365, dur=1.0)

def seg_C2():
    ctl.click(*TAB_MAKE); W(1.5); ctl.click(693, 1107); W(1); ctl.move(960, 850)

def seg_D():
    ctl.click(*TAB_SHEET); W(2); ctl.move(530, 330, dur=1.0); W(3); ctl.move(530, 578, dur=1.2); W(4)
    ctl.click(333, 1133); W(2); ctl.move(500, 378, dur=1.0); W(6)

def seg_F():
    ctl.click(*TAB_FINAL); W(1)
    ctl.click(687, 1133); W(1.5); ctl.move(1370, 695, dur=1.0); W(6)
    ctl.scroll(1000, 800, -4); W(5); ctl.scroll(1000, 800, 4); W(1)
    ctl.click(517, 1133); W(2); ctl.move(900, 500, dur=1.0); W(20)

def seg_G():
    ctl.click(*TAB_MAKE); W(1); ctl.move(960, 850)

SEGS = {"A": (24, seg_A), "B": (30, seg_B), "C1": (8, seg_C1), "C2": (80, seg_C2), "D": (22, seg_D),
        "F": (50, seg_F), "G": (22, seg_G)}
if False:
    for n in sys.argv[1:]:
        d, f = SEGS[n]; record("seg_" + n, d, f)

def seg_E():
    W(1); ctl.click(437, 597); W(2.5); ctl.click(515, 447); W(2)
    ctl.move(700, 560, dur=1.0); W(2); ctl.move(700, 660, dur=1.5); W(2)
    ctl.click(535, 821); W(1.5); ctl.scroll(800, 700, -3); W(8)
    ctl.click(1077, 290); W(1)
SEGS["E"] = (28, seg_E)
if __name__ == "__main__" and sys.argv[1:] == ["E2"]:
    pass
if __name__ == "__main__":
    for n in sys.argv[1:]:
        d, f = SEGS[n]; record("seg_" + n, d, f)
