# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['UI.py'],  # Archivo principal
    pathex=[],  # Dejamos vacío como en el archivo funcional
    binaries=[],
    datas=[('./icon.png','./'),('./icon.ico','./')],  # Eliminamos `datas` si no es necesario
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=['libc.so.6'],
    noarchive=False,  # No cambiamos esta configuración
    optimize=0,  # Optimización mínima

)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,  # Incluimos binarios y datos como en el archivo funcional
    a.datas,
    [],
    name='TFG-Gestor_de_base_de_datos',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Dejamos UPX activado como en el archivo funcional
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Permite la consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=["icon.ico"],
)
