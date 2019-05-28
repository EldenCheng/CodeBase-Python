from pathlib import Path

dirpath = Path(r"D:\VBA\DIRTest")

if not dirpath.is_dir():
    dirpath.mkdir()