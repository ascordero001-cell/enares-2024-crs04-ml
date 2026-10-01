from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

EXPECTED_SHA256 = "AE6D141A40497D8FB55E4FCF924726BBD1E65CF6321B4B341747725C0FA304CB"
STYLE_BLOCK = re.compile(r"<style(?:\s[^>]*)?>(.*?)</style>", re.IGNORECASE | re.DOTALL)
DARK_MODE_MARKERS = ("prefers-color-scheme:dark", 'data-theme="dark"')


def _rule_start(css: str, position: int) -> int:
    return (
        max(
            css.rfind("}", 0, position),
            css.rfind("{", 0, position),
            css.rfind(";", 0, position),
        )
        + 1
    )


def _strip_dark_mode(css: str) -> str:
    for marker in DARK_MODE_MARKERS:
        while (position := css.find(marker)) != -1:
            start = _rule_start(css, position)
            opening = css.find("{", position)
            if opening == -1:
                raise SystemExit(f"Regla de modo oscuro sin bloque: {marker}")
            depth = 0
            for end in range(opening, len(css)):
                if css[end] == "{":
                    depth += 1
                elif css[end] == "}":
                    depth -= 1
                    if depth == 0:
                        break
            else:
                raise SystemExit(f"Bloque de modo oscuro sin cierre: {marker}")
            css = css[:start] + css[end + 1 :]
    return css


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument(
        "--adapter",
        type=Path,
        default=Path("app/assets/stage04_streamlit_adapter.css"),
    )
    parser.add_argument(
        "--destination",
        type=Path,
        default=Path("app/assets/stage04_mockup.css"),
    )
    args = parser.parse_args()

    actual_hash = _sha256(args.source)
    if actual_hash != EXPECTED_SHA256:
        raise SystemExit(
            "El HTML rector no coincide con la versión aprobada: "
            f"esperado={EXPECTED_SHA256}, actual={actual_hash}"
        )

    source = args.source.read_text(encoding="utf-8")
    blocks = [_strip_dark_mode(block).strip() for block in STYLE_BLOCK.findall(source)]
    if not blocks:
        raise SystemExit("El HTML rector no contiene bloques <style>.")
    adapter = args.adapter.read_text(encoding="utf-8").strip()
    generated = (
        "/* GENERADO DESDE LA MAQUETA RECTORA; NO EDITAR A MANO. */\n"
        f"/* source_sha256={actual_hash} */\n\n"
        "/* Modo oscuro de la maqueta omitido: Streamlit usa tema claro. */\n\n"
        + "\n\n".join(blocks)
        + "\n\n/* ADAPTADOR STREAMLIT 1.64.0 */\n"
        + adapter
        + "\n"
    )
    args.destination.parent.mkdir(parents=True, exist_ok=True)
    args.destination.write_text(generated, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
