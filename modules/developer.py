# Voxueg modul: Developer
from core.utils import *

D = "Developer"

@feat(D, "Validasi JSON")
def _(): json.loads(ask("JSON")); out("JSON valid")

@feat(D, "Minify JSON")
def _(): out(json.dumps(json.loads(ask("JSON")), separators=(",", ":"), ensure_ascii=False))

@feat(D, "Epoch sekarang")
def _(): out(int(time.time()))

@feat(D, "Epoch ke tanggal")
def _(): out(datetime.fromtimestamp(int(ask("Epoch"))).strftime("%Y-%m-%d %H:%M:%S"))

@feat(D, "Tanggal ke epoch")
def _(): out(int(datetime.strptime(ask("Tanggal (YYYY-MM-DD HH:MM:SS)"), "%Y-%m-%d %H:%M:%S").timestamp()))

@feat(D, "Timestamp ISO 8601")
def _(): out(datetime.now().astimezone().isoformat())

@feat(D, "Tes regex")
def _():
    p, t = ask("Pola regex"), ask("Teks")
    m = re.findall(p, t)
    out(f"{len(m)} cocok: {m}")

@feat(D, "Diff dua file")
def _():
    import difflib
    a = open(ask("File 1"), errors="replace").read().splitlines()
    b = open(ask("File 2"), errors="replace").read().splitlines()
    out("\n".join(difflib.unified_diff(a, b, lineterm="")) or "Sama persis")

@feat(D, "HTML escape")
def _():
    import html; out(html.escape(ask("Teks")))

@feat(D, "HTML unescape")
def _():
    import html; out(html.unescape(ask("Teks")))

@feat(D, "Versi git")
def _(): sh("git --version")

@feat(D, "Status git sebuah folder")
def _(): sh(f"git -C {ask('Folder repo')} status -sb")

@feat(D, "Buat .gitignore")
def _():
    t = ask("Jenis (python/node)").lower()
    isi = {"python": "__pycache__/\n*.pyc\n.env\nvenv/\n", "node": "node_modules/\n.env\nnpm-debug.log\n"}.get(t)
    if not isi: out("Pilih python atau node"); return
    if os.path.exists(".gitignore"): out(".gitignore sudah ada, tidak ditimpa."); return
    open(".gitignore", "w").write(isi); out("Dibuat: .gitignore")

@feat(D, "CSV ke JSON")
def _():
    import csv
    rows = list(csv.DictReader(open(ask("File CSV"), newline="", encoding="utf-8")))
    out(json.dumps(rows[:20], indent=2, ensure_ascii=False))

@feat(D, "Cek sintaks file Python")
def _():
    import py_compile; py_compile.compile(ask("File .py"), doraise=True); out("Sintaks OK")

@feat(D, "Server HTTP lokal")
def _():
    p = ask("Port (default 8000)") or "8000"
    out("Ctrl+C untuk berhenti")
    try: subprocess.run([sys.executable, "-m", "http.server", p])
    except KeyboardInterrupt: pass
