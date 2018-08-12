import subprocess
import zipfile
from pathlib import Path

import requests
from pkg_resources import parse_version


class Updater:
    download_url = None
    remote_version = None
    local_version = None
    file = None

    def __init__(self):
        self.get_local_version()
        self.get_remote_version()
        self.get_filename()

    def get_local_version(self):
        self.local_version = parse_version(Path('version').read_text().strip())

    def get_remote_version(self):
        data = requests.get('https://api.github.com/repos/Tusky/KoDiscord/releases/latest').json()
        self.download_url = data['assets'][0]['browser_download_url']
        self.remote_version = parse_version(data['tag_name'])

    def is_there_an_update(self):
        return self.local_version < self.remote_version

    def get_filename(self):
        folder = Path('update')
        if not folder.exists():
            folder.mkdir()
        self.file = folder / self.download_url.split('/')[-1]

    def download_package(self):
        if not self.file.exists():
            r = requests.get(self.download_url)
            self.file.write_bytes(r.content)

    def extract_update(self):
        with zipfile.ZipFile(str(self.file), "r") as file:
            file.extractall("update")
        self.file.unlink()

    @staticmethod
    def update_kodiscord():
        subprocess.Popen(['updater.bat'], creationflags=subprocess.CREATE_NEW_CONSOLE)


if __name__ == '__main__':
    updater = Updater()
    if updater.is_there_an_update():
        updater.download_package()
        updater.extract_update()
        updater.update_kodiscord()
