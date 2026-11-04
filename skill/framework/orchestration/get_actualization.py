#!/usr/bin/env python3
"""Check for, and download, the actualization module.

Standalone on purpose: it uses only the standard library and lives inside
framework/orchestration/, so it still works when only the orchestration module
is installed. The module is needed to add tools, agents or skills to the
ecosystem (framework/actualization/update_ecosystem.py).

    python get_actualization.py --check     # exit 0 if present, 3 if missing
    python get_actualization.py             # ask, then download it
    python get_actualization.py --yes       # download without asking

Files are only downloaded and extracted; nothing is executed. Review
update_ecosystem.py before running it, and pin --ref to a tag or commit SHA
when you want a reproducible download.
"""

from __future__ import annotations

import argparse
import io
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

REPO = "Sudo-Vire/Omniagents"
DEFAULT_REF = "master"
UPSTREAM_SUBPATH = ("skill", "framework", "actualization")
MARKER = "update_ecosystem.py"
FRAMEWORK_DIR = Path(__file__).resolve().parent.parent
TARGET = FRAMEWORK_DIR / "actualization"


def is_present(target: Path | None = None) -> bool:
    return ((target or TARGET) / MARKER).is_file()


def warning(target: Path | None = None) -> str:
    target = target or TARGET
    return (
        f"AVISO: falta el módulo de actualización ({target}). Sin él no se pueden añadir "
        "herramientas, agentes ni skills al ecosistema.\n"
        f'  Descárgalo con: python "{Path(__file__).resolve()}"\n'
        f"  O instala la skill completa: npx skills add {REPO} --skill omniagents-orchestration"
    )


def extract(archive: zipfile.ZipFile, target: Path) -> int:
    """Extract only the actualization folder, rejecting paths that escape the target."""
    count = 0
    target = target.resolve()
    prefix = UPSTREAM_SUBPATH
    for info in archive.infolist():
        parts = PurePosixPath(info.filename).parts[1:]
        if info.is_dir() or parts[: len(prefix)] != prefix or len(parts) == len(prefix):
            continue
        relative = parts[len(prefix):]
        if any(part in ("..", "") for part in relative) or PurePosixPath(*relative).is_absolute():
            raise ValueError(f"Unsafe path in archive: {info.filename}")
        destination = target.joinpath(*relative).resolve()
        destination.relative_to(target)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with archive.open(info) as source, open(destination, "wb") as out:
            shutil.copyfileobj(source, out)
        count += 1
    return count


def download(ref: str, target: Path | None = None) -> int:
    target = target or TARGET
    url = f"https://codeload.github.com/{REPO}/zip/{ref}"
    print(f"Descargando {url}")
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read()
    with tempfile.TemporaryDirectory() as tmp:
        staged = Path(tmp) / "actualization"
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            count = extract(archive, staged)
        if count == 0 or not (staged / MARKER).is_file():
            raise ValueError(f"el archivo descargado no contiene skill/framework/actualization/{MARKER}")
        if target.exists():
            shutil.rmtree(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(staged, target)
    return count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="solo comprueba si el módulo está presente")
    parser.add_argument("--yes", action="store_true", help="descarga sin preguntar")
    parser.add_argument("--ref", default=DEFAULT_REF, help=f"rama, etiqueta o SHA (por defecto {DEFAULT_REF})")
    args = parser.parse_args(argv)

    if is_present():
        print(f"OK: el módulo de actualización ya está en {TARGET}")
        return 0
    if args.check:
        print(warning(), file=sys.stderr)
        return 3
    if not args.yes:
        if not (sys.stdin.isatty() and sys.stdout.isatty()):
            print(warning(), file=sys.stderr)
            print("  Terminal no interactiva: repite con --yes para descargarlo.", file=sys.stderr)
            return 3
        print(warning())
        if input(f"¿Descargar {REPO}@{args.ref} en {TARGET}? (s/N): ").strip().lower() != "s":
            print("Cancelado; no se ha descargado nada.")
            return 3
    try:
        count = download(args.ref)
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        print(f"ERROR: no se pudo descargar el módulo ({error}).", file=sys.stderr)
        return 1
    print(f"Hecho: {count} archivos en {TARGET}")
    utils = FRAMEWORK_DIR.parent / "dependencies" / "utils" / "check_utils.txt"
    if not utils.is_file():
        print(
            "Nota: falta dependencies/utils/check_utils.txt, así que el actualizador no podrá "
            f"registrar recursos. Instala la skill completa: npx skills add {REPO} --skill omniagents-orchestration"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
