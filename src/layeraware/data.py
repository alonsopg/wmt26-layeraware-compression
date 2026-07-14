from pathlib import Path

def lines(path): return Path(path).read_text().splitlines()

def validate_parallel(src, ref=None):
    source = lines(src)
    if ref is not None and len(source) != len(lines(ref)):
        raise ValueError("source/reference line count mismatch")
    return len(source)
