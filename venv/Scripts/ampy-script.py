#!"E:\Python Projects\uPython\workSpace\Hydrometer\venv\Scripts\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'adafruit-ampy==1.0.5','console_scripts','ampy'
__requires__ = 'adafruit-ampy==1.0.5'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('adafruit-ampy==1.0.5', 'console_scripts', 'ampy')()
    )
