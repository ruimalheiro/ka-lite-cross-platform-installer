# -*- mode: python -*-

from kivy.tools.packaging.pyinstaller_hooks import install_hooks
install_hooks(globals())

a = Analysis(['mytest.py'],
             pathex=['C:\\Users\\Rui\\Desktop\\ka-lite-cross-platform-installer'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
             
for d in a.datas:
    if 'pyconfig' in d[0]: 
        a.datas.remove(d)
        break
        
pyz = PYZ(a.pure)

tree = Tree('KA-lite-files')

exe = EXE(pyz,
          a.scripts,
          a.binaries,          
          [('ka_lite_installer.kv', 'C:\\Users\\Rui\\Desktop\\ka-lite-cross-platform-installer\\ka_lite_installer.kv', 'DATA'),
           ('logo32.png', 'C:\\Users\\Rui\\Desktop\\ka-lite-cross-platform-installer\\images\\logo32.png', 'DATA')],
          tree,
          a.zipfiles,
          a.datas,
          name='KALiteSetup.exe',
          debug=True,
          strip=None,
          upx=False,
          console=True,
          icon='images\\logo48.ico')
