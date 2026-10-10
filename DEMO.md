# TacticalVision desktop demonstration

This folder contains a new standalone desktop application (`demo.py`) that is separate from the existing stub modules under `src/`.

## Run on Windows

Install Python 3.10+ from python.org, ensuring Tkinter is included (standard Windows Python installers include it), then run:

```powershell
py -3 demo.py
```

No third-party Python packages are required. The interface has six pages:

- **ESP** — simulated 2D bounding boxes, synthetic labels, health bars and distances.
- **AIM TRAINING** — a non-interactive crosshair visualization.
- **CASE** — a mock container catalog and filters.
- **ITEM** — a sample item catalog and filters.
- **RADAR** — animated 2D radar driven by the same simulated entities as the ESP preview.
- **MISC** — pause/resume, settings and data-source diagnostics.

## Scope and safety

All displayed targets are **synthetic**. The demonstration has no dependency on Delta Force and does not access game memory, protected processes, drivers, DMA hardware, KMBOX, or input-control APIs. It does not bypass anti-cheat, operate on a multiplayer game's hidden entities, or control aiming.

The original `src/` modules are unchanged. This PR does not claim to turn the repository's existing placeholders into functional game cheats.

## Optional Windows EXE packaging

```powershell
py -3 -m pip install pyinstaller
py -3 -m PyInstaller --noconfirm --onefile --windowed --name TacticalVision-Lab demo.py
```

Look for `dist/TacticalVision-Lab.exe`. Build on Windows for a Windows executable.

## Next engineering steps

Use a typed replay schema for authorized recordings; move scene drawing into reusable components; implement config persistence and test resize, DPI scaling and rendering performance. Do not attach unauthorized game memory readers or automated game input.
