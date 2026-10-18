# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['study_balancer.py'],
    pathex=['D:\\THARUN PROJECT\\VERSION_3_WORKPLACE'],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('study_routine_data.json', '.'),
        ('tharun_diary_format.json', '.'),
        ('tharun_exam_portions.json', '.'),
        ('time_extension_audit.json', '.'),
        ('student_error_bank.json', '.'),
        ('EXAM_SYSTEM_V3', 'EXAM_SYSTEM_V3')
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    hiddenimports=[
        'pywinstyles',
        'customtkinter',
        'PIL',
        'PIL.ImageTk',
        'PIL.ImageFilter',
        'google.genai',
        'pypdf',
        'reportlab',
        'reportlab.lib.pagesizes',
        'reportlab.lib.colors',
        'reportlab.lib.styles',
        'reportlab.platypus',
        'exam_engine_v3',
        'host_exam_ui',
        'shinobi_ui',
        'schedule_engine',
        'winocr'
    ],
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
    name='ScholasticPulse_V3',
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
