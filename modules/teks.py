# Voxueg modul: Teks
from core.utils import *

T = "Teks"

MORSE = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..',
         'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
         'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
         '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....',
         '7': '--...', '8': '---..', '9': '----.'}

@feat(T, "Base64 encode")
def _(): out(base64.b64encode(ask("Teks").encode()).decode())

@feat(T, "Base64 decode")
def _(): out(base64.b64decode(ask("Base64")).decode(errors="replace"))

@feat(T, "Hex encode")
def _(): out(binascii.hexlify(ask("Teks").encode()).decode())

@feat(T, "Hex decode")
def _(): out(binascii.unhexlify(ask("Hex")).decode(errors="replace"))

@feat(T, "URL encode")
def _(): out(urllib.parse.quote(ask("Teks")))

@feat(T, "URL decode")
def _(): out(urllib.parse.unquote(ask("Teks")))

@feat(T, "Hash MD5")
def _(): out(hashlib.md5(ask("Teks").encode()).hexdigest())

@feat(T, "Hash SHA1")
def _(): out(hashlib.sha1(ask("Teks").encode()).hexdigest())

@feat(T, "Hash SHA256")
def _(): out(hashlib.sha256(ask("Teks").encode()).hexdigest())

@feat(T, "Hash SHA512")
def _(): out(hashlib.sha512(ask("Teks").encode()).hexdigest())

@feat(T, "HURUF BESAR")
def _(): out(ask("Teks").upper())

@feat(T, "huruf kecil")
def _(): out(ask("Teks").lower())

@feat(T, "Balik teks")
def _(): out(ask("Teks")[::-1])

@feat(T, "Hitung kata & karakter")
def _():
    t = ask("Teks")
    out(f"Kata: {len(t.split())}\nKarakter: {len(t)}")

@feat(T, "Buat slug")
def _(): out(re.sub(r"[^a-z0-9]+", "-", ask("Teks").lower()).strip("-"))

@feat(T, "ROT13")
def _(): out(codecs.encode(ask("Teks"), "rot13"))

@feat(T, "Teks ke Morse")
def _(): out(" ".join(MORSE.get(c, "?") if c != " " else "/" for c in ask("Teks").upper()))

@feat(T, "Morse ke teks")
def _():
    r = {v: k for k, v in MORSE.items()}
    out("".join(" " if c == "/" else r.get(c, "?") for c in ask("Morse (pisah spasi, kata pakai /)").split()))

@feat(T, "Teks ke biner")
def _(): out(" ".join(f"{b:08b}" for b in ask("Teks").encode()))

@feat(T, "Sandi Caesar")
def _():
    t, k = ask("Teks"), int(ask("Geser"))
    out("".join(chr((ord(c) - (65 if c.isupper() else 97) + k) % 26 + (65 if c.isupper() else 97)) if c.isalpha() else c for c in t))

@feat(T, "Rapikan JSON")
def _(): out(json.dumps(json.loads(ask("JSON")), indent=2, ensure_ascii=False))

@feat(T, "Hash CRC32")
def _(): out(f"{binascii.crc32(ask('Teks').encode()) & 0xffffffff:08x}")

@feat(T, "Base32 encode")
def _(): out(base64.b32encode(ask("Teks").encode()).decode())

@feat(T, "Base32 decode")
def _(): out(base64.b32decode(ask("Base32")).decode(errors="replace"))

@feat(T, "Frekuensi huruf")
def _():
    from collections import Counter
    c = Counter(ch for ch in ask("Teks").lower() if ch.isalpha())
    out("\n".join(f"{k}: {v}" for k, v in c.most_common()))

@feat(T, "Title Case")
def _(): out(ask("Teks").title())

@feat(T, "Rapikan spasi ganda")
def _(): out(" ".join(ask("Teks").split()))

@feat(T, "Cek palindrom")
def _():
    t = re.sub(r"[^a-z0-9]", "", ask("Teks").lower())
    out("Palindrom" if t == t[::-1] and t else "Bukan palindrom")

@feat(T, "Acak urutan kata")
def _():
    w = ask("Teks").split(); random.shuffle(w); out(" ".join(w))

@feat(T, "Teks ke kode ASCII")
def _(): out(" ".join(str(ord(c)) for c in ask("Teks")))
