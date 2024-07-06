# -*- mode: python ; coding: utf-8 -*-

import glob

a = Analysis(
    ['menu.py'],
    pathex=['C:\\Users\\詹景棠\\citypet'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

audio_folders = glob.glob(r'C:\\Users\\詹景棠\\citypet\\audio\\*')
audio_files = glob.glob(r'C:\\Users\\詹景棠\\citypet\\audio\\*\\*.mp3')
for folder in audio_folders:
    for file in audio_files:
        a.datas += [(f"audio\\{file.split(os.sep)[-2]}\\{file.split(os.sep)[-1]}", file, 'DATA')]

image_folders = glob.glob(r'C:\\Users\\詹景棠\\citypet\\images\\*')
image_files = glob.glob(r'C:\\Users\\詹景棠\\citypet\\images\\*\\*.png')
for folder in image_folders:
    for file in image_files:
        a.datas += [(f"images\\{file.split(os.sep)[-2]}\\{file.split(os.sep)[-1]}", file, 'DATA')]

a.datas += [('pet.py', "C:\\Users\\詹景棠\\citypet\\pet.py", 'DATA')]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='menu',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
