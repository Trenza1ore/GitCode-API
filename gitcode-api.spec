# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for a one-file gitcode-api CLI (entry: scripts/pyinstaller_cli_entry.py)."""

from pathlib import Path

block_cipher = None
spec_dir = Path(SPECPATH)

a = Analysis(
    [str(spec_dir / "scripts" / "pyinstaller_cli_entry.py")],
    pathex=[str(spec_dir)],
    binaries=[],
    datas=[(str(spec_dir / "gitcode_api" / "version.txt"), "gitcode_api")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="gitcode-api",
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
