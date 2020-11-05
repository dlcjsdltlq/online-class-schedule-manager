# -*- mode: python ; coding: utf-8 -*-


specpath = os.path.dirname(os.path.abspath(SPEC))
block_cipher = None


a = Analysis(['main.py'],
             pathex=['.'],
             binaries=[],
             datas=[
                ('./resources/json/schedule_sample.json', 'resources/json'),
                ('./resources/json/schedule_schema.json', 'resources/json'),
                ('./resources/ui/ui_main_window.ui', 'resources/ui'),
                ('./resources/ui/ui_memo_window.ui', 'resources/ui'),
                ('./resources/ui/ui_schedule_window.ui', 'resources/ui'),
                ('./resources/icon/logo.ico', 'resources/icon')
                ],
             hiddenimports=['plyer.platforms.win.notification'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='online-class-schedule-manager v1.2.1',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon = './resources/icon/logo.ico'
          )
