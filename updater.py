import requests
import subprocess
import zipfile
from pathlib import Path
from pkg_resources import parse_version


class Updater:
    download_url = None
    remote_version = None
    local_version = None
    file = None
    version = '0.6.8'

    def __init__(self):
        self.get_local_version()
        self.get_remote_version()
        self.get_filename()

    def get_local_version(self):
        self.local_version = parse_version(self.version)

    def get_remote_version(self):
        try:
            data = requests.get('https://api.github.com/repos/Tusky/KoDiscord/releases/latest').json()
        except requests.exceptions.ConnectionError:
            self.remote_version = self.local_version
        else:
            self.download_url = data['assets'][0]['browser_download_url']
            self.remote_version = parse_version(data['tag_name'])

    def is_there_an_update(self):
        return self.local_version < self.remote_version

    def get_filename(self):
        from util.config import BASE_DIR
        folder = Path(f'{BASE_DIR}\\update')
        if not folder.exists():
            folder.mkdir(exist_ok=True)
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
