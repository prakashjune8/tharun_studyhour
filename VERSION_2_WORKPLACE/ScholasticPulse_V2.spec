# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['study_balancer.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('study_routine_data.json', '.'),
        ('tharun_diary_format.json', '.'),
        ('tharun_exam_portions.json', '.'),
        ('time_extension_audit.json', '.'),
        ('student_error_bank.json', '.')
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
    name='ScholasticPulse_V2',
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
