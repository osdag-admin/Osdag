# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['osdag_validator_cli\\entry.py'],
    pathex=[],
    binaries=[],
    datas=[('Osdag\\src\\osdag\\data\\ResourceFiles', 'osdag\\data\\ResourceFiles')],
    hiddenimports=['osdag', 'osdag.data', 'osdag_validator'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='osdag-val',
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
