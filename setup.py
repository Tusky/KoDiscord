import os.path
from pathlib import Path

from cx_Freeze import setup, Executable

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

base = 'Win32GUI'

kodiscord = Executable('app.py', base=base, icon='kodi-icon.ico', targetName="KoDiscord.exe")
updater = Executable('updater.py', base=None, icon='kodi-icon.ico', targetName='KoDiscord-updater.exe')

executables = [kodiscord, updater]

packages = ['asyncio', 'idna', 'pypresence', 'requests', 'threading', 'typing', 'pystray', 'PIL', 'pkg_resources']
options = {
    'build_exe': {
        'packages': packages,
        'include_files': ['kodi-icon.ico', 'LICENSE', 'web', 'version', 'updater.bat'],
        'include_msvcr': True
    },
}
version = Path('version').read_text().strip()

setup(
    name="KoDiscord",
    options=options,
    version=version.replace('b', '.'),
    author='Richard Hajdu',
    author_email='tuskone16@gmail.com',
    url='https://github.com/Tusky/KoDiscord',
    description='Sends your currently watched Movie or TV Show from Kodi to discord.',
    executables=executables
)
