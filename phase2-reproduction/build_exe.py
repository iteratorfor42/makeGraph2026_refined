#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_exe.py
------------
makegraph.py를 Windows 실행파일(makegraph.exe)로 패키징한다.

반드시 Windows 환경에서 실행해야 한다 (PyInstaller는 크로스 컴파일을
지원하지 않으므로, Linux/Mac에서 실행하면 그 OS용 실행파일이 만들어진다).

사용법:
    python build_exe.py

결과:
    dist/makegraph.exe   (단일 파일, 콘솔 프로그램)

요구 사항:
    - Windows 10/11
    - Python 3.9 이상 (64bit 권장)
    - 인터넷 연결 (최초 1회, pyinstaller 설치용)
"""

import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENTRY_SCRIPT = HERE / "makegraph.py"
DIST_DIR = HERE / "dist"
BUILD_DIR = HERE / "build"
SPEC_FILE = HERE / "makegraph.spec"


def run(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def ensure_pyinstaller() -> None:
    try:
        import PyInstaller  # noqa: F401
        print("PyInstaller가 이미 설치되어 있습니다.")
    except ImportError:
        print("PyInstaller가 없습니다. 설치를 진행합니다...")
        run([sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller"])


def clean_previous_build() -> None:
    for path in (DIST_DIR, BUILD_DIR, SPEC_FILE):
        if path.is_dir():
            shutil.rmtree(path)
            print(f"이전 빌드 삭제: {path}")
        elif path.is_file():
            path.unlink()
            print(f"이전 spec 삭제: {path}")


def build() -> None:
    if not ENTRY_SCRIPT.exists():
        print(f"오류: {ENTRY_SCRIPT} 파일을 찾을 수 없습니다.", file=sys.stderr)
        sys.exit(1)

    run([
        sys.executable, "-m", "PyInstaller",
        "--onefile",              # 단일 exe 파일로 묶기
        "--console",              # 콘솔(CLI) 프로그램
        "--name", "makegraph",
        "--distpath", str(DIST_DIR),
        "--workpath", str(BUILD_DIR),
        "--specpath", str(HERE),
        str(ENTRY_SCRIPT),
    ])

    exe_path = DIST_DIR / "makegraph.exe"
    if exe_path.exists():
        print(f"\n빌드 완료: {exe_path}")
        print("사용 예:")
        print(f"  {exe_path.name} sample.lst")
        print(f"  {exe_path.name} sample.lst -o result.html")
    else:
        print("빌드는 종료되었지만 makegraph.exe를 찾지 못했습니다. "
              "위 PyInstaller 로그를 확인하세요.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    ensure_pyinstaller()
    clean_previous_build()
    build()
