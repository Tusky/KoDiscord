from cx_Freeze import setup, Executable
import os.path

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

base = 'Win32GUI'

executables = [Executable('app.py', base=base, icon='kodi-icon.ico', targetName="KoDiscord.exe")]

packages = ['asyncio', 'idna', 'pypresence', 'requests', 'threading', 'typing', 'pystray', 'PIL']
options = {
    'build_exe': {
        'packages': packages,
    },
}

setup(
    name="KoDiscord",
    options=options,
    version="0.1",
    description='Sends your currently watched Movie or TV Show from Kodi to discord.',
    executables=executables
)
