from pathlib import Path
import re


def instruhandle(path):
    ls = []
    root_directory = Path(path)
    for d in root_directory.glob("*"):
        w = re.split('[^a-zA-Z]', str(d))
        ls.append(w[4])
    res = sorted([*set(ls)])
    return res
