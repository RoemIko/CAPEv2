# Copyright (C) 2014 Optiv, Inc. (brad.spengler@optiv.com)
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.common.abstracts import Package


class Chrome(Package):
    """Chrome analysis package."""

    PATHS = [
        ("ProgramFiles", "Google", "Chrome", "Application", "chrome.exe"),
        ("LOCALAPPDATA", "Chromium", "Application", "chrome.exe"),
    ]
    summary = "Opens the URL in Google Chrome."
    description = """Uses 'chrome.exe --disable-features=RendererCodeIntegrity "<url>"' to open the supplied url."""

    def start(self, url):
        chrome = self.get_path("Google")
        # pass the URL instead of a filename in this case
        return self.execute(chrome, f'"{url}"', url)
