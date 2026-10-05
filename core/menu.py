# Voxueg menu utama
from core.utils import *
from core import ui

PER = 14
_first = [True]


def banner():
    ui.banner(animate=_first[0]); _first[0] = False


def pause():
    t = ui.T()
    input(f"\n  {ui.col(t['acc'])}[Enter]{ui.RESET} kembali ")


def run(cat, name, fn):
    os.system("clear")
    ui.apply_theme()
    ui.titlebar(f"{cat} › {name}")
    print()
    safe(fn)()
    print()
    ui.rule()
    pause()


def search():
    banner()
    ui.titlebar("Cari fitur")
    print()
    q = ask("Kata kunci").lower()
    hits = [x for x in F if q and (q in x[1].lower() or q in x[0].lower())]
    if not hits:
        out("Tidak ditemukan."); pause(); return
    page = 0
    while True:
        os.system("clear")
        ui.titlebar("Hasil pencarian", f"{len(hits)} fitur")
        print()
        chunk = hits[page * PER:(page + 1) * PER]
        for i, (c, n, _) in enumerate(chunk, 1): print(ui.item(i, n, c))
        print()
        ui.hint(*([("n", "lanjut")] if (page + 1) * PER < len(hits) else []), *([("p", "balik")] if page else []), ("0", "kembali"))
        s = ask("Pilih").lower()
        if s == "0": return
        if s == "n" and (page + 1) * PER < len(hits): page += 1
        elif s == "p" and page: page -= 1
        elif s.isdigit() and 1 <= int(s) <= len(chunk):
            c, n, f = chunk[int(s) - 1]; run(c, n, f)


def theme():
    banner()
    ui.titlebar("Pilih tema")
    print()
    keys = list(ui.THEMES)
    for i, k in enumerate(keys, 1):
        t = ui.THEMES[k]
        sw = "".join(ui.col(g) + "██" for g in t["grad"]) + ui.RESET
        print(ui.item(i, f"{t['nama']:<6} {sw}"))
    print()
    s = ask("Nomor tema (0 = batal)")
    if s.isdigit() and 1 <= int(s) <= len(keys):
        ui.save_theme(keys[int(s) - 1]); ui.apply_theme()


def category(cat):
    items = [x for x in F if x[0] == cat]
    page, pages = 0, (len(items) + PER - 1) // PER
    while True:
        os.system("clear")
        ui.apply_theme()
        ui.titlebar(f"Voxueg › {cat}", f"{len(items)} fitur")
        print()
        base = page * PER
        for i, (_, n, _) in enumerate(items[base:base + PER], 1): print(ui.item(base + i, n))
        print()
        if pages > 1: print(f"  {ui.DIM}halaman {page + 1}/{pages}{ui.RESET}")
        ui.hint(*([("n", "lanjut")] if page + 1 < pages else []), *([("p", "balik")] if page else []), ("0", "kembali"))
        s = ask("Pilih").lower()
        if s == "0": return
        if s == "n" and page + 1 < pages: page += 1
        elif s == "p" and page: page -= 1
        elif s.isdigit() and 1 <= int(s) <= len(items):
            c, n, f = items[int(s) - 1]; run(c, n, f)


def main():
    cats = list(dict.fromkeys(c for c, _, _ in F))
    while True:
        banner()
        for i, c in enumerate(cats, 1):
            print(ui.item(i, c, str(sum(1 for x in F if x[0] == c))))
        print()
        ui.hint(("s", "cari"), ("t", "tema"), ("0", "keluar"))
        p = ask("Pilih").lower()
        if p == "0":
            print(f"\n  Sampai jumpa! {ui.DIM}- {DEV}{ui.RESET}\n"); break
        if p == "s": search(); continue
        if p == "t": theme(); continue
        if p.isdigit() and 1 <= int(p) <= len(cats): category(cats[int(p) - 1])
