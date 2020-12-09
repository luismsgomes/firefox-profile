import json
import os
import sys

from datetime import datetime
from functools import lru_cache

import lz4.block


__version__ = "0.0.3"


class FirefoxTab:
    def __init__(self, url, title, last_accessed):
        self.url = url
        self.title = title
        self.last_accessed = last_accessed

    def to_json(self):
        return dict(
            last_accessed=self.last_accessed.isoformat(), url=self.url, title=self.title
        )


class FirefoxWindow:
    def __init__(
        self,
        tabs,
        workspace,
        zindex,
        size,
        position,
        mode,
    ):
        self.tabs = tabs
        self.workspace = workspace
        self.zindex = zindex
        self.size = size
        self.position = position
        self.mode = mode

    def to_json(self):
        return dict(
            tabs=[tab.to_json() for tab in self.tabs],
            workspace=self.workspace,
            zindex=self.zindex,
            size=self.size,
            position=self.position,
            mode=self.mode,
        )


class FirefoxRecoveryData:
    def __init__(self, data):
        self.data = data

    @property
    @lru_cache(maxsize=1)
    def windows(self):
        windows = []
        for window in self.data["windows"]:
            window_tabs = []
            for tab in window["tabs"]:
                entry = tab["entries"][tab["index"] - 1]
                window_tabs.append(
                    FirefoxTab(
                        last_accessed=datetime.fromtimestamp(
                            tab["lastAccessed"] / 1000
                        ),
                        url=entry["url"],
                        title=entry["title"],
                    )
                )
            windows.append(
                FirefoxWindow(
                    tabs=window_tabs,
                    workspace=window.get("workspaceID", None),
                    zindex=window.get("zIndex", None),
                    size=(window.get("width", None), window.get("height", None)),
                    position=(window.get("screenX", None), window.get("screenY", None)),
                    mode=window.get("sizemode", None),
                )
            )
        return windows


class FirefoxProfile:
    def __init__(self, name, hash, path):
        self.name = name
        self.hash = hash
        self.path = path

    def to_json(self):
        return dict(name=self.name, hash=self.hash, path=self.path)

    @property
    def recovery_file_path(self):
        return os.path.join(self.path, "sessionstore-backups", "recovery.jsonlz4")

    def get_recovery_data(self):
        if not os.path.exists(self.recovery_file_path):
            return None
        with open(self.recovery_file_path, "rb") as f:
            # the first 8 bytes in recovery.jsonlz4 should contain
            # the string mozLz40
            assert f.read(8) == b"mozLz40\0"
            # after these 8 bytes the file is a lz4 stream
            compressed_data = f.read()
        data = lz4.block.decompress(compressed_data)
        return FirefoxRecoveryData(json.loads(data.decode("utf-8")))

    def __str__(self):
        return f"profile {self.name}"

    @staticmethod
    def get_profiles(profiles_dir=None):
        if profiles_dir is None:
            profiles_dir = FirefoxProfile.get_profiles_dir()
        with os.scandir(profiles_dir) as entries:
            for entry in entries:
                if (
                    entry.is_dir()
                    and not entry.name.startswith(".")
                    and "." in entry.name
                    and os.path.isfile(
                        os.path.join(profiles_dir, entry.name, "times.json")
                    )
                ):
                    profile_hash, _, profile_name = entry.name.partition(".")
                    if not profile_name:
                        continue
                    profile_path = os.path.join(profiles_dir, entry.name)
                    yield FirefoxProfile(
                        name=profile_name, hash=profile_hash, path=profile_path
                    )

    @staticmethod
    def get_profiles_dir():
        if sys.platform.startswith("win"):
            return os.path.expandvars("%APPDATA%\\Mozilla\\Firefox\\Profiles")
        if sys.platform.startswith("darwin"):
            return os.path.expanduser("~/Library/Application Support/Firefox/Profiles")
        return os.path.expanduser("~/.mozilla/firefox")


def main():
    json_data = []
    for profile in FirefoxProfile.get_profiles():
        recovery_data = profile.get_recovery_data()
        if recovery_data is None:
            continue
        json_data.append(
            dict(
                profile=profile.to_json(),
                windows=[window.to_json() for window in recovery_data.windows],
            )
        )

    print(json.dumps(json_data, indent=4))


if __name__ == "__main__":
    main()
