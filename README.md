# SCC Player Cam

A small Windows app for players' PCs that sends their webcam to the SCC HUD on the GFX PC
(League, VALORANT, Call of Duty and Rocket League HUDs all receive it).

## Install

Download and run **[SCC-Player-Cam-Setup.exe](https://github.com/owenbparker/playercam_SCC/releases/latest/download/SCC-Player-Cam-Setup.exe)**.
It installs to `C:\SCC Player Cam` with a desktop shortcut, without an administrator prompt,
and always installs the newest release.

Players enter the GFX PC's address (for example `192.168.2.40`), or let the app find the HUD on
the network, then pick their game, team, role and camera. The app remembers all of it and updates
itself when a new release is out.

Players who'd rather not install anything can open the HUD's **Player cam link** in Chrome or Edge
instead (`https://<GFX PC>:8779/cam` for League). The app is the same page without the
certificate warning.

## Releases

Every push builds the app on Windows (GitHub Actions) and publishes release `v2.0.<run>` with
`PlayerCam-windows.zip` (what the app's updater downloads) and `SCC-Player-Cam-Setup.exe`.
A commit with `[no release]` in its message builds and tests without publishing.

Player Cam used to be built with the League HUD (releases up to v1.0.89 of LeagueHUDSCC).
Versions here start at 2.0 so those installs update to this repo's releases; the League HUD
releases also carry a copy of the latest Player Cam files for older installs.

## From source

    pip install pywebview
    python -m playercam              # or: python PlayerCam.py
    python -m unittest discover -s tests

## Layout

    playercam/app.py        the app: serves web/cam.html on 127.0.0.1 and opens it in a window
    playercam/camprops.py   camera settings (exposure, focus, ...) through Windows
    playercam/discover.py   finds HUDs on the local network
    playercam/updater.py    checks this repo's latest release and updates in place
    web/cam.html            the cam page (also served by the League HUD as its /cam link)
    PlayerCam.spec          PyInstaller build
    installer/              Inno Setup installer
