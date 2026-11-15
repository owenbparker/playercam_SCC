import json
import os
import tempfile
import unittest
import urllib.request

from playercam import app as camapp
from playercam import updater
from playercam.updater import Updater


class PlayerCamAppTests(unittest.TestCase):
    def test_riot_account_without_the_riot_client(self):
        self.assertIn("isn't running", camapp.riot_account("/nonexistent/lockfile")["error"])
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "lockfile")
            with open(path, "w") as f:
                f.write("Riot Client:1:1:pw:https")      # nothing listening on port 1
            self.assertIn("Sign in", camapp.riot_account(path)["error"])

    def test_page_and_logos_served(self):
        httpd = camapp.serve(Updater())
        try:
            port = httpd.server_address[1]
            for path in ("/cam", "/update.js", "/fonts/Inter.ttf", "/assets/playercam_icon.png", "/assets/games/lol.svg",
                         "/assets/games/valorant.svg", "/assets/games/cod.svg", "/assets/games/rl.svg"):
                with urllib.request.urlopen(f"http://127.0.0.1:{port}{path}", timeout=5) as r:
                    self.assertTrue(r.read())
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/riot/account", timeout=10) as r:
                self.assertIn("error", json.loads(r.read()))
        finally:
            httpd.shutdown()

    def test_bundled_files_match_the_spec(self):
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(root, "PlayerCam.spec"), encoding="utf-8") as f:
            spec = f.read()
        for rel in camapp.FILES.values():
            self.assertTrue(os.path.isfile(os.path.join(root, "web", rel)), rel)
            self.assertIn(f'"{os.path.basename(rel)}"', spec, f"{rel} isn't packed in PlayerCam.spec")


class UpdaterTests(unittest.TestCase):
    def test_updates_come_from_this_repo(self):
        self.assertEqual(updater.REPO, "owenbparker/playercam_SCC")
        u = Updater()
        self.assertEqual((u.asset_name, u.exe), ("PlayerCam-windows.zip", "PlayerCam.exe"))

    def test_version_two_is_newer_than_the_league_numbered_ones(self):
        self.assertTrue(updater.is_newer("v2.0.3", "v1.0.89"))
        self.assertFalse(updater.is_newer("v1.0.95", "v2.0.1"))


class PlayerCamPriorityTest(unittest.TestCase):
    def test_descendants_any_depth(self):
        procs = [(1, 0), (10, 1), (11, 10), (12, 11), (13, 10), (20, 2), (0, 0)]
        self.assertEqual(sorted(camapp.descendants(procs, 10)), [11, 12, 13])
        self.assertEqual(camapp.descendants(procs, 99), [])


if __name__ == "__main__":
    unittest.main()
