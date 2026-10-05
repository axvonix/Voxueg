# Voxueg UI: tema warna, banner besar, kotak, dan bilah judul
import os, re, json, time, shutil
from core.utils import NAME, DEV, VER, F, C

CFG = os.path.expanduser("~/.voxueg/config.json")
RESET, BOLD, DIM = "\033[0m", "\033[1m", "\033[2m"

THEMES = {
    "neon":  {"nama": "Neon",  "grad": [51, 45, 39, 99, 165, 201], "acc": 51,  "num": 213, "ok": 84,  "err": 203},
    "hijau": {"nama": "Hijau", "grad": [46, 47, 48, 49, 41, 35],   "acc": 46,  "num": 120, "ok": 84,  "err": 203},
    "api":   {"nama": "Api",   "grad": [196, 202, 208, 214, 220, 226], "acc": 214, "num": 220, "ok": 120, "err": 196},
    "ungu":  {"nama": "Ungu",  "grad": [93, 99, 105, 141, 177, 213], "acc": 141, "num": 183, "ok": 120, "err": 203},
    "laut":  {"nama": "Laut",  "grad": [27, 33, 39, 45, 51, 87],   "acc": 45,  "num": 159, "ok": 120, "err": 203},
    "mono":  {"nama": "Mono",  "grad": [255, 252, 249, 246, 243, 240], "acc": 255, "num": 250, "ok": 255, "err": 250},
}

FONT = {
    "V": ["█   █", "█   █", "█   █", " █ █ ", "  █  "],
    "O": [" ███ ", "█   █", "█   █", "█   █", " ███ "],
    "X": ["█   █", " █ █ ", "  █  ", " █ █ ", "█   █"],
    "U": ["█   █", "█   █", "█   █", "█   █", " ███ "],
    "E": ["█████", "█    ", "████ ", "█    ", "█████"],
    "G": [" ████", "█    ", "█  ██", "█   █", " ████"],
}


def col(n): return f"\033[38;5;{n}m"
def vis(s): return len(re.sub(r"\033\[[0-9;]*m", "", s))
def width(): return max(34, min(shutil.get_terminal_size((44, 24)).columns - 2, 58))


def load_theme():
    try: return json.load(open(CFG)).get("tema", "neon")
    except Exception: return "neon"


def save_theme(k):
    os.makedirs(os.path.dirname(CFG), exist_ok=True)
    json.dump({"tema": k}, open(CFG, "w"))


def T(): return THEMES.get(load_theme(), THEMES["neon"])


def apply_theme():
    t = T()
    C["c"], C["g"], C["r"] = col(t["acc"]), col(t["num"]), col(t["err"])
    return t


def box(lines, color=None):
    t = T(); color = color or col(t["acc"]); w = width()
    inner = w - 2
    print(f"{color}╭{'─' * inner}╮{RESET}")
    for ln in lines:
        print(f"{color}│{RESET}{ln}{' ' * max(inner - vis(ln), 0)}{color}│{RESET}")
    print(f"{color}╰{'─' * inner}╯{RESET}")


def titlebar(left, right=""):
    t = T(); a = col(t["acc"]); w = width()
    mid = max(w - vis(left) - vis(right) - 6, 1)
    print(f"{a}╭─ {BOLD}{left}{RESET}{a} {'─' * mid} {right} ─╮{RESET}")


def rule():
    print(f"{col(T()['acc'])}{DIM}{'─' * width()}{RESET}")


def big_banner(animate=False):
    t = T(); rows = ["", "", "", "", ""]
    for i, ch in enumerate("VOXUEG"):
        for r in range(5):
            rows[r] += col(t["grad"][i]) + BOLD + FONT[ch][r] + RESET + " "
    pad = " " * max((width() - 36) // 2, 1)
    print()
    for r in rows:
        print(pad + r)
        if animate: time.sleep(0.06)
    print()


def banner(animate=False):
    os.system("clear")
    t = apply_theme(); a = col(t["acc"])
    big_banner(animate)
    box([f" {BOLD}{NAME}{RESET} v{VER}   {DIM}·{RESET}   {col(t['num'])}{len(F)}{RESET} fitur",
         f" Dev: {a}{DEV}{RESET}   {DIM}·{RESET}   tema: {t['nama']}"])
    print()


def item(no, label, right=""):
    t = T(); w = width()
    left = f"  {col(t['num'])}{'[' + str(no) + ']':>4}{RESET} {label}"
    gap = max(w - vis(left) - vis(right) - 1, 1)
    return left + " " * gap + (f"{DIM}{right}{RESET}" if right else "")


def hint(*pairs):
    t = T()
    print("  " + "   ".join(f"{col(t['num'])}[{k}]{RESET} {v}" for k, v in pairs))
