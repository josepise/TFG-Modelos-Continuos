# -*- mode: python ; coding: utf-8 -*-

datas = [
    ('ContinuousModelGenerator/resources/img/add_1.png', 'ContinuousModelGenerator/resources/img'),
    ('ContinuousModelGenerator/resources/img/edit_1.png', 'ContinuousModelGenerator/resources/img'),
    ('ContinuousModelGenerator/resources/img/delete_1.png', 'ContinuousModelGenerator/resources/img'),
]

a = Analysis(
    ['ContinuousModelGenerator/generator.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['PIL._tkinter_finder','reportlab'],
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
    name='GeneratorSimulator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
