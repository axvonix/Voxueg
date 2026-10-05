# Voxueg modul: Hitung & Konversi
from core.utils import *

H = "Hitung & Konversi"

OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
       ast.Pow: operator.pow, ast.Mod: operator.mod, ast.FloorDiv: operator.floordiv, ast.USub: operator.neg}

def calc(n):
    if isinstance(n, ast.Expression): return calc(n.body)
    if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)): return n.value
    if isinstance(n, ast.BinOp) and type(n.op) in OPS: return OPS[type(n.op)](calc(n.left), calc(n.right))
    if isinstance(n, ast.UnaryOp) and type(n.op) in OPS: return OPS[type(n.op)](calc(n.operand))
    raise ValueError("Ekspresi tidak valid")

def convert(table):
    v, a, b = float(ask("Nilai")), ask(f"Dari {list(table)}"), ask("Ke")
    out(f"{v * table[a] / table[b]:g} {b}")

@feat(H, "Kalkulator")
def _(): out(calc(ast.parse(ask("Ekspresi"), mode="eval")))

@feat(H, "Konversi suhu")
def _():
    v, a, b = float(ask("Nilai")), ask("Dari (C/F/K)").upper(), ask("Ke (C/F/K)").upper()
    c = {"C": v, "F": (v - 32) * 5 / 9, "K": v - 273.15}[a]
    out(f"{ {'C': c, 'F': c * 9 / 5 + 32, 'K': c + 273.15}[b]:.2f} {b}")

@feat(H, "Konversi panjang")
def _(): convert({"mm": .001, "cm": .01, "m": 1, "km": 1000, "inch": .0254, "ft": .3048, "mil": 1609.344})

@feat(H, "Konversi berat")
def _(): convert({"mg": 1e-6, "g": .001, "kg": 1, "ton": 1000, "oz": .0283495, "lb": .453592})

@feat(H, "Cek bilangan prima")
def _():
    n = int(ask("Angka"))
    out("Prima" if n > 1 and all(n % i for i in range(2, int(n ** .5) + 1)) else "Bukan prima")

@feat(H, "Faktorial")
def _(): out(math.factorial(int(ask("Angka"))))

@feat(H, "Deret Fibonacci")
def _():
    a, b, r = 0, 1, []
    for _ in range(int(ask("Banyak suku"))): r.append(a); a, b = b, a + b
    out(", ".join(map(str, r)))

@feat(H, "Desimal ke biner")
def _(): out(bin(int(ask("Desimal")))[2:])

@feat(H, "Biner ke desimal")
def _(): out(int(ask("Biner"), 2))

@feat(H, "Desimal ke hex")
def _(): out(hex(int(ask("Desimal")))[2:])

@feat(H, "Hex ke desimal")
def _(): out(int(ask("Hex"), 16))

@feat(H, "Persentase")
def _():
    p, n = float(ask("Persen")), float(ask("Dari angka"))
    out(f"{p}% dari {n:g} = {p * n / 100:g}")

@feat(H, "Hitung umur")
def _():
    d = datetime.strptime(ask("Tanggal lahir (YYYY-MM-DD)"), "%Y-%m-%d").date()
    t = date.today()
    out(f"{t.year - d.year - ((t.month, t.day) < (d.month, d.day))} tahun ({(t - d).days} hari)")

@feat(H, "FPB & KPK")
def _():
    a, b = int(ask("Angka 1")), int(ask("Angka 2"))
    out(f"FPB: {math.gcd(a, b)}\nKPK: {a * b // math.gcd(a, b)}")

@feat(H, "Hitung BMI")
def _():
    kg, cm = float(ask("Berat (kg)")), float(ask("Tinggi (cm)"))
    b = kg / (cm / 100) ** 2
    k = "Kurus" if b < 18.5 else "Normal" if b < 25 else "Berlebih" if b < 30 else "Obesitas"
    out(f"BMI {b:.1f} ({k})")

@feat(H, "Bagi tagihan")
def _():
    t, n = float(ask("Total tagihan")), int(ask("Jumlah orang"))
    out(f"Per orang: {t / n:,.2f}")

@feat(H, "Simulasi cicilan")
def _():
    p, r, n = float(ask("Pokok")), float(ask("Bunga % per tahun")) / 1200, int(ask("Jumlah bulan"))
    m = p / n if r == 0 else p * r / (1 - (1 + r) ** -n)
    out(f"Cicilan/bulan: {m:,.2f}\nTotal bayar: {m * n:,.2f}")

@feat(H, "Tabel perkalian")
def _():
    n = int(ask("Angka"))
    out("\n".join(f"{n} x {i} = {n * i}" for i in range(1, 11)))

@feat(H, "Angka ke romawi")
def _():
    n, r = int(ask("Angka (1-3999)")), ""
    for v, s in [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"),
                 (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]:
        while n >= v: r += s; n -= v
    out(r)

@feat(H, "Romawi ke angka")
def _():
    m, t, p = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}, 0, 0
    for c in reversed(ask("Romawi").upper()):
        v = m[c]; t += v if v >= p else -v; p = max(p, v)
    out(t)

@feat(H, "Konversi ukuran data")
def _(): convert({"B": 1, "KB": 1024, "MB": 1024 ** 2, "GB": 1024 ** 3, "TB": 1024 ** 4})

@feat(H, "Konversi kecepatan")
def _(): convert({"m/s": 1, "km/h": 1 / 3.6, "mph": .44704, "knot": .514444})

@feat(H, "Durasi detik ke jam:menit:detik")
def _():
    s = int(ask("Detik")); out(f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}")

@feat(H, "Hari dari tanggal")
def _(): out(datetime.strptime(ask("Tanggal (YYYY-MM-DD)"), "%Y-%m-%d").strftime("%A"))

@feat(H, "Kalender bulan tertentu")
def _(): out(calendar.month(int(ask("Tahun")), int(ask("Bulan (1-12)"))))
