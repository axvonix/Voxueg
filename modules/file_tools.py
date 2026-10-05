# Voxueg modul: File
from core.utils import *

FL = "File"

@feat(FL, "Daftar isi folder")
def _(): sh(f"ls -lah {ask('Folder (default .)') or '.'}")

@feat(FL, "Cari file")
def _(): sh(f"find {ask('Folder awal (default .)') or '.'} -iname '*{ask('Nama')}*' 2>/dev/null | head -50")

@feat(FL, "Ukuran folder")
def _(): sh(f"du -sh {ask('Folder (default .)') or '.'}")

@feat(FL, "Hash file (SHA256)")
def _():
    h = hashlib.sha256()
    with open(ask("Path file"), "rb") as f:
        for c in iter(lambda: f.read(65536), b""): h.update(c)
    out(h.hexdigest())

@feat(FL, "Baca file")
def _(): out(open(ask("Path file"), errors="replace").read()[:3000])

@feat(FL, "Hitung baris file")
def _(): out(sum(1 for _ in open(ask("Path file"), errors="replace")))

@feat(FL, "Tambah catatan")
def _():
    os.makedirs(os.path.dirname(NOTES), exist_ok=True)
    with open(NOTES, "a") as f: f.write(f"[{datetime.now():%Y-%m-%d %H:%M}] {ask('Catatan')}\n")
    out("Tersimpan.")

@feat(FL, "Baca catatan")
def _(): out(open(NOTES).read() if os.path.exists(NOTES) else "Belum ada catatan.")

@feat(FL, "Backup folder ke ZIP")
def _():
    src = ask("Folder")
    dst = f"{os.path.basename(os.path.abspath(src))}_{datetime.now():%Y%m%d_%H%M%S}.zip"
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for r, _, fs in os.walk(src):
            for f in fs: z.write(os.path.join(r, f))
    out(f"Dibuat: {dst}")
