"""Empaqueta el tema como Luxo_theme-vX.Y.Z.zip.

La version vive en config/settings_schema.json (theme_info.theme_version),
que es donde Shopify la lee para mostrarla en el admin.

  python build-theme.py           -> empaqueta la version actual
  python build-theme.py patch     -> 1.0.0 -> 1.0.1  (correcciones)
  python build-theme.py minor     -> 1.0.1 -> 1.1.0  (secciones o ajustes nuevos)
  python build-theme.py major     -> 1.1.0 -> 2.0.0  (rediseno)
"""

import json
import os
import sys
import zipfile

NAME = "Luxo_theme"
FOLDERS = ["assets", "blocks", "config", "layout", "locales", "sections", "snippets", "templates"]
ROOT = os.path.dirname(os.path.abspath(__file__))
SCHEMA = os.path.join(ROOT, "config", "settings_schema.json")


def read_version():
    with open(SCHEMA, encoding="utf-8") as fh:
        data = json.load(fh)
    return data, data[0]["theme_version"]


def bump(version, part):
    major, minor, patch = (int(n) for n in version.split("."))
    if part == "major":
        major, minor, patch = major + 1, 0, 0
    elif part == "minor":
        minor, patch = minor + 1, 0
    elif part == "patch":
        patch += 1
    else:
        sys.exit(f"Parte desconocida: {part} (usa major, minor o patch)")
    return f"{major}.{minor}.{patch}"


def main():
    data, version = read_version()

    if len(sys.argv) > 1:
        version = bump(version, sys.argv[1])
        data[0]["theme_version"] = version
        data[0]["theme_name"] = NAME
        with open(SCHEMA, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print(f"theme_version -> {version}")

    out = os.path.join(ROOT, f"{NAME}-v{version}.zip")
    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for folder in FOLDERS:
            base = os.path.join(ROOT, folder)
            if not os.path.isdir(base):
                continue
            for dirpath, dirnames, filenames in os.walk(base):
                dirnames[:] = [d for d in dirnames if d not in (".git", "__MACOSX")]
                for filename in filenames:
                    if filename == ".DS_Store" or filename.endswith(".zip"):
                        continue
                    full = os.path.join(dirpath, filename)
                    zf.write(full, os.path.relpath(full, ROOT).replace("\\", "/"))
                    count += 1

    size = os.path.getsize(out) / 1048576
    print(f"{os.path.basename(out)}  —  {count} archivos, {size:.1f} MB")


if __name__ == "__main__":
    main()
