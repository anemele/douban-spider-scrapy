import time
from pathlib import Path

_BASE_PATH_FILE = Path('./savepath.txt')
if not _BASE_PATH_FILE.exists():
    BASE_PATH = Path('./data')
else:
    BASE_PATH = Path(_BASE_PATH_FILE.read_text(encoding='utf-8'))

if not BASE_PATH.exists():
    BASE_PATH.mkdir()

# info 文件保存格式：日期格式 2022-10-24.csv
INFO_PATH = BASE_PATH / f'{time.strftime("%Y-%m-%d", time.localtime())}.csv'

# 图片保存位置
PIC_PATH = BASE_PATH / 'pictures'

if not PIC_PATH.exists():
    PIC_PATH.mkdir()
