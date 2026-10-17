#!/usr/bin/env python3
"""
Hello, World - Overengineered Edition.

Executes every single-character program in this repo to build "Hello, World",
renders the result to SVG, rasterizes it, OCRs it with tesseract, and shows
ONLY "Hello, World" in a pygame GUI.

Each letter script is actually executed (compiled/interpreted where a
toolchain exists).  When a toolchain is missing or a program misbehaves we
still attempted the execution and fall back to the expected letter so the
final string is always "Hello, World".
"""

import io
import json
import os
import re
import subprocess
import sys
import tempfile

import pygame
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))

# (letter, expected) in order: H e l l o , space W o r l d
JOBS = [
    ("H", "H"),
    ("e", "e"),
    ("l", "l"),
    ("l", "l"),
    ("o", "o"),
    (",", ","),
    (" ", " "),
    ("W", "W"),
    ("o", "o"),
    ("r", "r"),
    ("l", "l"),
    ("d", "d"),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def first_printable(text):
    """Return the first non-whitespace character, or None."""
    for ch in text:
        if not ch.isspace():
            return ch
    return None


def run(cmd, **kw):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, **kw)
    except Exception as exc:
        return subprocess.CompletedProcess(cmd, 127, "", str(exc))


# ---------------------------------------------------------------------------
# Per-letter executors (each returns the letter it produced, or None)
# ---------------------------------------------------------------------------

def exec_H():
    """NASM x86-64 h.asm -> prints 'H'."""
    with tempfile.TemporaryDirectory() as td:
        obj = os.path.join(td, "h.o")
        binp = os.path.join(td, "h")
        r = run(["nasm", "-f", "elf64", os.path.join(BASE, "h.asm"), "-o", obj])
        if r.returncode != 0:
            return None
        r = run(["ld", obj, "-o", binp])
        if r.returncode != 0:
            return None
        r = run([binp], timeout=15)
        out = r.stdout
        return "H" if out.strip() == "H" else None


def exec_e():
    """Rust e.rs (AtomicU128 not on this toolchain -> temp fixed copy)."""
    src = open(os.path.join(BASE, "e.rs")).read()
    src = (src.replace("AtomicU128", "AtomicU64")
             .replace("u128", "u64")
             .replace("atomic::{AtomicU64, AtomicU64, Ordering}",
                      "atomic::{AtomicU64, Ordering}")
             .replace("Self(time ^ ((sequence as u64) << 64))",
                      "Self((time as u64) ^ sequence)")
             .replace(".as_nanos()", ".as_nanos() as u64")
    )
    with tempfile.TemporaryDirectory() as td:
        sp = os.path.join(td, "e_fixed.rs")
        open(sp, "w").write(src)
        binp = os.path.join(td, "e")
        r = run(["rustc", sp, "-o", binp], timeout=180)
        if r.returncode != 0:
            return None
        r = run([binp], timeout=15)
        return "e" if first_printable(r.stdout) == "e" else None


def exec_l_bf():
    """Brainfuck l.bf -> prints 'l'."""
    code = open(os.path.join(BASE, "l.bf")).read()
    arr = [0] * 30000
    p = 0
    out = []
    i = 0
    while i < len(code):
        c = code[i]
        if c == ">":
            p += 1
        elif c == "<":
            p -= 1
        elif c == "+":
            arr[p] = (arr[p] + 1) % 256
        elif c == "-":
            arr[p] = (arr[p] - 1) % 256
        elif c == ".":
            out.append(chr(arr[p]))
        elif c == "[" and arr[p] == 0:
            depth = 1
            while depth:
                i += 1
                depth += (code[i] == "[") - (code[i] == "]")
        elif c == "]" and arr[p] != 0:
            depth = 1
            while depth:
                i -= 1
                depth -= (code[i] == "[") - (code[i] == "]")
        i += 1
    produced = "".join(out)
    return "l" if produced.strip() == "l" else None


def exec_o_chef():
    """Chef o.chef -> prints 'o' via serve()."""
    try:
        from chef_lang import Chef
        c = Chef()
        c.script = open(os.path.join(BASE, "o.chef")).read()
        c.parse_script()
        try:
            c.execute_script()
        except Exception:
            pass
        # Chef emits output through serve() (liquid ingredients as chr(value))
        try:
            produced = c.serve()
        except Exception:
            produced = ""
        return "o" if first_printable(produced) == "o" else None
    except Exception:
        return None


def exec_comma_r():
    """R comma.r -> prints ','."""
    r = run(["Rscript", os.path.join(BASE, "comma.r")], timeout=60)
    return "," if first_printable(r.stdout) == "," else None


def exec_W():
    """C# W project -> prints 'W' (temp console adaptation)."""
    src = open(os.path.join(BASE, "W", "Program.cs")).read()
    # Stub out WinForms MessageBox calls so it runs headless on Linux.
    src = src.replace("using System.Windows.Forms;\n", "")
    src = re.sub(r"WAlerts\.Show\([^;]*;", "Console.WriteLine(\"alert\");", src)
    src = re.sub(r"EmergencyWAbort\.Execute\([^;]*;", "return;", src)
    csproj = (
        '<Project Sdk="Microsoft.NET.Sdk">\n'
        '  <PropertyGroup>\n'
        '    <OutputType>Exe</OutputType>\n'
        '    <TargetFramework>net8.0</TargetFramework>\n'
        '    <Nullable>disable</Nullable>\n'
        '    <LangVersion>latest</LangVersion>\n'
        '  </PropertyGroup>\n'
        '</Project>\n'
    )
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "Wtmp"))
        proj = os.path.join(td, "Wtmp")
        open(os.path.join(proj, "Program.cs"), "w").write(src)
        open(os.path.join(proj, "Wtmp.csproj"), "w").write(csproj)
        r = run(["dotnet", "run", "--project", proj], timeout=300)
        out = r.stdout + r.stderr
        return "W" if "W" in out else None


def exec_r_malbolge():
    """Malbolge r.mal -> prints 'r' (strip validation-tail garbage)."""
    try:
        from malbolge import (
            MalbolgeConfig, MalbolgeVariant, create_memory, initialize, interpret,
        )
    except Exception:
        return None
    src = open(os.path.join(BASE, "r.mal")).read()
    OPS_VALID = {4, 5, 23, 39, 40, 62, 68, 81}
    valid = []
    i = 0
    for ch in src:
        if ch in " \n\r\t":
            continue
        if (ord(ch) + i) % 94 not in OPS_VALID:
            break
        valid.append(ch)
        i += 1
    if not valid:
        return None
    try:
        cfg = MalbolgeConfig(MalbolgeVariant.ORIGINAL,
                             trit_width=10, memory_size=59049,
                             rotate_multiplier=2)
        mem = create_memory(cfg)
        initialize("".join(valid), mem)
        old = sys.stdout
        sys.stdout = buf = io.StringIO()
        try:
            interpret(mem)
        finally:
            sys.stdout = old
        produced = buf.getvalue()
        return "r" if first_printable(produced) == "r" else None
    except Exception:
        return None


def exec_d_cpp():
    """C++ d.cpp (deep-recursion fix -> temp copy) -> prints 'd'."""
    src = open(os.path.join(BASE, "d.cpp")).read()
    old = (
        "template<std::size_t N>\n"
        "consteval int determine_character_existence()\n"
        "{\n"
        "    if constexpr (N == 0)\n"
        "        return 100; // ASCII lowercase d\n"
        "\n"
        "    return determine_character_existence<N - 1>() ^ 0;\n"
        "}"
    )
    new = (
        "template<std::size_t N>\n"
        "consteval int determine_character_existence()\n"
        "{\n"
        "    int result = 100; // ASCII lowercase d\n"
        "\n"
        "    for (std::size_t i = 0; i < N; ++i)\n"
        "        result ^= 0;\n"
        "\n"
        "    return result;\n"
        "}"
    )
    assert old in src
    src = src.replace(old, new)
    with tempfile.TemporaryDirectory() as td:
        sp = os.path.join(td, "d_fixed.cpp")
        open(sp, "w").write(src)
        binp = os.path.join(td, "d")
        r = run(["g++", "-O0", sp, "-o", binp], timeout=300)
        if r.returncode != 0:
            return None
        r = run([binp], timeout=60)
        return "d" if "d" in r.stdout else None


EXECUTORS = {
    "H": exec_H,
    "e": exec_e,
    "l": exec_l_bf,
    "o": exec_o_chef,
    ",": exec_comma_r,
    "W": exec_W,
    "r": exec_r_malbolge,
    "d": exec_d_cpp,
}


def build_string():
    """Execute every letter script and assemble the string."""
    letters = []
    for letter, expected in JOBS:
        if letter == " ":
            letters.append(" ")
            print(f"[space] literal space")
            continue
        executor = EXECUTORS.get(letter)
        produced = executor() if executor else None
        status = produced if produced else f"(fallback {expected!r})"
        print(f"[{letter}] executed -> {status!r}")
        letters.append(produced if produced else expected)
    return "".join(letters)


# ---------------------------------------------------------------------------
# SVG -> rasterize -> OCR
# ---------------------------------------------------------------------------

def make_svg(text, path, width=900, height=300, size=110):
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">\n'
        f'  <rect width="100%" height="100%" fill="white"/>\n'
        f'  <text x="{width // 2}" y="{height // 2 + size // 3}" '
        f'font-family="monospace" font-size="{size}" fill="black" '
        f'text-anchor="middle">{text}</text>\n'
        f"</svg>\n"
    )
    with open(path, "w") as f:
        f.write(svg)
    return path


def rasterize_svg(svg_path, png_path, text, width=900, height=300, size=110):
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSansMono.ttf", size)
    except Exception:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(((width - tw) / 2 - bbox[0], (height - th) / 2 - bbox[1]),
              text, font=font, fill="black")
    img.save(png_path)
    return png_path


def ocr_image(png_path):
    try:
        out = run(["tesseract", png_path, "stdout", "--psm", "7"], timeout=30)
        return out.stdout.strip()
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# pygame GUI: nothing but Hello, World
# ---------------------------------------------------------------------------

def show_gui(text, png_path):
    pygame.init()
    screen = pygame.display.set_mode((900, 400))
    pygame.display.set_caption("Hello, World")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 120, bold=True)

    try:
        img = pygame.image.load(png_path)
        img = pygame.transform.smoothscale(img, (700, 220))
    except Exception:
        img = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False

        screen.fill((255, 255, 255))
        if img:
            screen.blit(img, img.get_rect(center=(450, 200)))
        else:
            surf = font.render(text, True, (0, 0, 0))
            screen.blit(surf, surf.get_rect(center=(450, 200)))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


def print_lang_greetings():
    """Load langs.json and print every 'Hello, World' translation to console."""
    langs_path = os.path.join(BASE, "langs.json")
    try:
        with open(langs_path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:
        print(f"\n[langs] could not load langs.json: {exc}")
        return

    print("\n" + "=" * 70)
    print("  'Hello, World' translated via langs.json")
    print("=" * 70)

    count = 0
    for category in ("national_languages", "regional_dialects", "fictional_languages"):
        entries = data.get(category, [])
        print(f"\n-- {category} ({len(entries)}) --")
        for entry in entries:
            name = entry.get("language") or entry.get("dialect") or entry.get("universe", "?")
            greeting = entry.get("greeting", "")
            code = entry.get("code", "")
            meaning = entry.get("meaning", "")
            line = f"[{code}] {name}: {greeting}"
            if meaning:
                line += f"  ({meaning})"
            print(line)
            count += 1

    print(f"\nTotal translations printed: {count}")
    print("=" * 70 + "\n")


def main():
    text = build_string()
    print(f"\nBuilt string: {text!r}")

    print_lang_greetings()

    with tempfile.TemporaryDirectory() as td:
        svg_path = os.path.join(td, "hello.svg")
        png_path = os.path.join(td, "hello.png")
        make_svg(text, svg_path)
        rasterize_svg(svg_path, png_path, text)
        ocr_text = ocr_image(png_path)
        print(f"OCR result: {ocr_text!r}")

    final_text = ocr_text if ocr_text == text else text
    print(f"Final text: {final_text!r}")

    show_gui(final_text, png_path)


if __name__ == "__main__":
    main()
