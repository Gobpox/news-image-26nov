# SPDX-License-Identifier: MIT
"""Competition entry point: copy entry.png to the output directory.

Standard library only. Verifies the copy is byte-identical to the
repository image (SHA-256) before reporting success.
"""
import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    src = HERE / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "entry.png"
    shutil.copyfile(src, dst)
    h_src = hashlib.sha256(src.read_bytes()).hexdigest()
    h_dst = hashlib.sha256(dst.read_bytes()).hexdigest()
    assert h_src == h_dst, "copy differs from source"
    print(f"entry.png -> {dst} sha256={h_dst} bytes={dst.stat().st_size}")


if __name__ == "__main__":
    main()
