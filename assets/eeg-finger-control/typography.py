"""Resolve local CJK and Latin fonts; never download or embed licensed fonts."""
import os
from pathlib import Path
from functools import lru_cache
from PIL import ImageFont

@lru_cache(maxsize=128)
def font(size, bold=False, latin=False):
    key=('MOTION_FONT_LATIN_BOLD' if bold else 'MOTION_FONT_LATIN') if latin else ('MOTION_FONT_BOLD' if bold else 'MOTION_FONT_REGULAR')
    win=Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts'
    if latin:
        candidates=[win/('arialbd.ttf' if bold else 'arial.ttf'),Path('/usr/share/fonts/truetype/dejavu')/('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'),Path('/System/Library/Fonts/Supplemental')/('Arial Bold.ttf' if bold else 'Arial.ttf')]
    else:
        candidates=[win/('msyhbd.ttc' if bold else 'msyh.ttc'),Path('/usr/share/fonts/opentype/noto')/('NotoSansCJK-Bold.ttc' if bold else 'NotoSansCJK-Regular.ttc'),Path('/System/Library/Fonts/PingFang.ttc')]
    if os.environ.get(key):candidates.insert(0,Path(os.environ[key]))
    for path in candidates:
        if path.is_file():return ImageFont.truetype(str(path),size)
    raise FileNotFoundError(f'No suitable font found. Set {key} to an installed font file supporting this text.')
