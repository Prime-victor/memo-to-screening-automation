import os, subprocess, textwrap, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "segs")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo.mp4")

# segment: (file, trim_start, trim_end, speed, [(t0, t1, caption)])  times are in OUTPUT seconds of the segment
PLAN = [
 ("seg_A", 0, 21, 1.0, [
   (0, 7, "Memo-to-Screening Automation - AI Analyst Case Study   |   Victor Kiptum"),
   (7, 14, "Problem: analysts copy data from investment memos into the TMS screening template by hand."),
   (14, 21, "Solution: a low-code Make.com workflow that extracts the data and fills the template automatically.")]),
 ("seg_B", 0, 28, 1.0, [
   (0, 8.5, "Step 1 - Google Drive watches an intake folder and downloads the new memo as plain text."),
   (8.5, 18, "Step 2 - Google Gemini (3.6 Flash) extracts key fields as structured JSON. Rule: never guess - return null if not stated."),
   (18, 28, "Step 3 - 13 Google Sheets modules each write one field into its exact template cell (e.g. company name -> B5).")]),
 ("seg_C1", 0, 7.5, 1.0, [
   (0, 7.5, "Live run - the template starts empty, with the placeholder 'ABC Ltd'.")]),
 ("seg_C2", 0, 23, 1.6, [
   (0, 14.4, "Run once:  Google Drive -> Gemini -> Google Sheets.  Gemini reads the memo in about 15 seconds.")]),
 ("seg_D", 0, 22, 1.0, [
   (0, 6, "Company, description, sector, funding, climate, 2X and security are filled in automatically."),
   (6, 12.5, "Country = Nigeria -> the template's own lookup returns Tier 1 automatically."),
   (12.5, 22, "Revenue 2022-2025 is populated, and the template's growth formulas calculate by themselves.")]),
 ("seg_E", 0, 25, 1.0, [
   (0, 12, "Gemini's output arrives already structured (JSON response mode) - no parsing module needed."),
   (12, 25, "It also flags issues itself: the memo says USD 10m senior debt in the intro, but USD 6m debt + USD 4m equity in the funding section.")]),
 ("seg_F", 0, 41, 1.0, [
   (0, 9, "The fully completed screening template: all financials mapped for 2022-2025F, with a source comment on every input."),
   (9, 18, "Preliminary score 87% -> 'Actively cultivate'.  Proposed: USD 6m senior secured facility, ~1.5x asset coverage."),
   (18, 29.5, "Review Flags: the 2025F balance sheet doesn't balance, EBITDA subtotals don't add up, and the cash flow doesn't reconcile."),
   (29.5, 41, "The memo claims 32% capital efficiency (on the loan book). On equity + debt it is ~22% -> scored 2, not 3.")]),
 ("seg_G", 0, 19, 1.0, [
   (0, 6.3, "AI suggests, analyst decides: risk scores and conflicting data stay with a human reviewer."),
   (6.3, 12.6, "Limitation: Gemini can return 503 'high demand' errors -> next step: automatic retries."),
   (12.6, 19, "Next: extend to every financial line, write flags to the sheet automatically, log each run. Details in the handover note.")]),
]

parts = []
for i, (name, a, b, speed, caps) in enumerate(PLAN):
    vf = [f"trim=start={a}:end={b}", "setpts=PTS-STARTPTS"]
    if speed != 1.0:
        vf.append(f"setpts=PTS/{speed}")
    for j, (t0, t1, txt) in enumerate(caps):
        tf = os.path.join(D, f"cap_{i}_{j}.txt")
        with open(tf, "w", encoding="utf-8") as f:
            f.write("\n".join(textwrap.wrap(txt, 62)))
        vf.append("drawtext=fontfile=arialbd.ttf:textfile=" + os.path.basename(tf) +
                  ":expansion=none:fontsize=38:fontcolor=white:line_spacing=10:box=1:boxcolor=black@0.72:boxborderw=22"
                  ":x=(w-text_w)/2:y=h-text_h-95" + f":enable='between(t,{t0},{t1})'")
    out = os.path.join(D, f"part_{i}.mp4")
    subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error", "-i", name + ".mp4", "-vf", ",".join(vf),
                    "-r", "15", "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", "-an",
                    os.path.basename(out)], cwd=D, check=True)
    parts.append(os.path.basename(out)); print("built", out)

with open(os.path.join(D, "list.txt"), "w") as f:
    f.writelines(f"file '{p}'\n" for p in parts)
subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "list.txt",
                "-c", "copy", "-movflags", "+faststart", OUT], cwd=D, check=True)
print("final", OUT)
