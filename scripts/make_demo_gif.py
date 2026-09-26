"""Run the offline demo and render actual terminal output with Pillow."""
from pathlib import Path
import subprocess
import sys
import textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = [
    ["list", "--industry", "general", "--call-type", "voicemail-amd"],
    ["lint", "prompts/voicemail-amd/generic-voicemail-and-amd.md"],
    ["render", "examples/demo.md", "--var", "company=Acme"],
]


def main() -> None:
    """Save a compact terminal animation without shell recording tools."""
    try:
        font = ImageFont.truetype("DejaVuSansMono.ttf", 16)
    except OSError:
        font = ImageFont.load_default()
    frames = []
    for args in COMMANDS:
        run = subprocess.run([sys.executable, "-m", "voice_agent_prompts", *args], cwd=ROOT, capture_output=True, text=True, check=True)
        lines = ["$ vap " + " ".join(args), ""]
        for line in run.stdout.splitlines():
            lines.extend(textwrap.wrap(line, width=92) or [""])
        # Show all output using terminal-sized pages.
        for start in range(0, len(lines), 23):
            frame = Image.new("RGB", (960, 620), "#0f172a")
            draw = ImageDraw.Draw(frame)
            draw.text((24, 20), "voice-agent-prompts | offline demo", font=font, fill="#67e8f9")
            draw.line((24, 54, 936, 54), fill="#475569", width=2)
            for n, line in enumerate(lines[start:start+23]):
                draw.text((24, 76+n*22), line, font=font, fill="#e2e8f0")
            frames.append(frame)
    dest = ROOT / "docs/demo.gif"
    dest.parent.mkdir(exist_ok=True)
    frames[0].save(dest, save_all=True, append_images=frames[1:], duration=3500, loop=0, optimize=True)
    if dest.stat().st_size >= 2_000_000:
        raise RuntimeError("Demo exceeds the file size budget")
    print(f"Saved {dest.relative_to(ROOT)} ({dest.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
