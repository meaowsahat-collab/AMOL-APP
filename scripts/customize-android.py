"""Run after `npx cap add android`: puts the Amol logo, icons and splash screen
into the generated Android project and colours the status bar green."""
import os
import shutil
import sys
import xml.dom.minidom

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, 'android', 'app', 'src', 'main', 'res')
SRC = os.path.join(ROOT, 'branding', 'android')
GREEN = '#0F3D2E'

if not os.path.isdir(RES):
    sys.exit('android project not found, run "npx cap add android" first')

# 1. icons (launcher, round, adaptive foreground) and splash images
shutil.copytree(SRC, RES, dirs_exist_ok=True)

# 2. adaptive icon background colour
with open(os.path.join(RES, 'values', 'ic_launcher_background.xml'), 'w', encoding='utf-8') as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
            f'    <color name="ic_launcher_background">{GREEN}</color>\n</resources>\n')

# 3. status bar, navigation bar and splash colours
styles = os.path.join(RES, 'values', 'styles.xml')
text = open(styles, encoding='utf-8').read()

old_main = '<item name="android:background">@null</item>'
new_main = (old_main + '\n        <item name="android:statusBarColor">' + GREEN + '</item>'
            '\n        <item name="android:windowLightStatusBar">false</item>')
old_splash = '<item name="android:background">@drawable/splash</item>'
new_splash = (old_splash + '\n        <item name="windowSplashScreenBackground">' + GREEN + '</item>')

for old, new in ((old_main, new_main), (old_splash, new_splash)):
    if old not in text:
        sys.exit('styles.xml changed upstream, could not find: ' + old)
    text = text.replace(old, new, 1)
xml.dom.minidom.parseString(text)  # fail early if the XML is broken
open(styles, 'w', encoding='utf-8').write(text)

print('Android branding applied')
