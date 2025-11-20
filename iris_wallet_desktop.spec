# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files
from PyInstaller.building.build_main import Analysis, PYZ, EXE, BUNDLE, COLLECT
from PyInstaller.utils.hooks import collect_dynamic_libs
print(sys.platform)

block_cipher = None
spec_file_path = os.path.abspath(sys.argv[0])
current_dir = os.path.dirname(spec_file_path)
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, 'src/utils'))
from src.version import __version__
from src.flavour import __network__
from src.utils.constant import APP_NAME, ORGANIZATION_DOMAIN
print(__version__)
print(__network__)

# Collect data files from pyqttoast, bip32utils, mnemonic, and cryptography
pyqttoast_datas = collect_data_files('pyqttoast')
rgb_lib_datas = collect_data_files('rgb_lib')
rgb_lib_binaries = collect_dynamic_libs('rgb_lib')

base_project_path = os.path.abspath(__name__)
print(base_project_path)
ln_node_binary = os.path.abspath(os.path.join(base_project_path, "../ln_node_binary", 'rgb-lightning-node'))
print(ln_node_binary)

if sys.platform.startswith('win'):
    ln_node_binary = os.path.abspath(os.path.join(base_project_path, "../ln_node_binary/rgb-lightning-node.exe"))
else:
    ln_node_binary = os.path.abspath(os.path.join(base_project_path, "../ln_node_binary/rgb-lightning-node"))

# Define data files
datas = [
    ('./src/assets/icons/*', './assets/icons/'),
    ('./src/views/qss/*.qss', './views/qss/'),
    ('./build_info.json', './build_info.json'),
    (ln_node_binary, './ln_node_binary/'),
] + pyqttoast_datas + rgb_lib_datas

# Common Analysis
a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=rgb_lib_binaries,
    datas=datas,
    hiddenimports=['pyqttoast', 'PySide6', 'bip32utils', 'mnemonic', 'importlib_metadata', 'hashlib', 'rgb_lib', 'keyring', 'keyrings', 'keyrings.alt', 'keyrings.alt.file'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        'unit_tests',
        'e2e_tests'
        ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = None

# Platform-specific EXE
if sys.platform == 'darwin':
    exe = EXE(
        pyz,
        a.scripts,
        exclude_binaries=True,
        name=APP_NAME,
        debug=False,
        strip=False,
        upx=True,
        console=False
    )
elif sys.platform.startswith('win'):
    icon_path = f'./src/assets/icons/{__network__}-icon.ico'
    exe = EXE(
        pyz,
        a.scripts,
        exclude_binaries=True,
        name=APP_NAME,
        debug=False,
        strip=False,
        upx=True,
        console=False,
        icon=icon_path
    )
elif sys.platform == 'linux':
    exe = EXE(
        pyz,
        a.scripts,
        exclude_binaries=True,
        name=APP_NAME,
        debug=False,
        strip=False,
        upx=True,
        console=False
    )

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    name=APP_NAME,
    strip=False,
    upx=True
)

# Build a .app bundle if on macOS
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name=f"{APP_NAME}.app",
        version=__version__,
        bundle_identifier=ORGANIZATION_DOMAIN,
        icon='./src/assets/icons/iriswallet.icns',
        info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSAppleScriptEnabled': False,
            'CFBundleVersion': __version__,
            'CFBundleShortVersionString': __version__,
            'CFBundleName': APP_NAME,
            'CFBundleDocumentTypes': [{
                'CFBundleTypeName': 'Iriswallet Document',
                'CFBundleTypeIconFile': 'iriswallet.icns',
                'LSItemContentTypes': [ORGANIZATION_DOMAIN],
                'LSHandlerRank': 'Owner'
            }]
        },
    )
