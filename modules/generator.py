# Voxueg modul: Generator
from core.utils import *

G = "Generator"

@feat(G, "Password acak")
def _():
    n = int(ask("Panjang (default 16)") or 16)
    out("".join(random.SystemRandom().choice(string.ascii_letters + string.digits + "!@#$%^&*") for _ in range(n)))

@feat(G, "UUID")
def _(): out(uuid.uuid4())

@feat(G, "Angka acak")
def _():
    a, b = int(ask("Min")), int(ask("Max"))
    out(random.randint(a, b))

@feat(G, "Lempar dadu")
def _(): out(f"Hasil: {random.randint(1, int(ask('Sisi (default 6)') or 6))}")

@feat(G, "Lempar koin")
def _(): out(random.choice(["Kepala", "Ekor"]))

@feat(G, "PIN acak")
def _(): out("".join(random.choice(string.digits) for _ in range(int(ask("Digit (default 6)") or 6))))

@feat(G, "Token hex")
def _():
    import secrets
    out(secrets.token_hex(int(ask("Byte (default 16)") or 16)))

@feat(G, "Warna acak")
def _():
    r, g, b = (random.randint(0, 255) for _ in range(3))
    out(f"#{r:02x}{g:02x}{b:02x}  rgb({r},{g},{b})")

@feat(G, "Lorem ipsum")
def _():
    w = "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore".split()
    out(" ".join(random.choice(w) for _ in range(int(ask("Jumlah kata (default 30)") or 30))).capitalize() + ".")

@feat(G, "Pilih acak dari daftar")
def _(): out(random.choice([x.strip() for x in ask("Daftar (pisah koma)").split(",")]))
