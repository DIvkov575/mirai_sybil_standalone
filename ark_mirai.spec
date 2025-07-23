# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['ark_mirai_run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('api/configs/', 'api/configs/'),
        ('main.py', '.'),
        ('static/', 'static/'),
        ('templates/', 'templates/'),
    ],
    hiddenimports=[
    'waitress',
    'gunicorn',
    ],
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
    name='ark_mirai',
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
