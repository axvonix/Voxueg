# Voxueg modul: Jaringan
from core.utils import *

N = "Jaringan"

@feat(N, "IP lokal")
def _():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    out(s.getsockname()[0]); s.close()

@feat(N, "IP publik")
def _(): out(get("https://api.ipify.org").read().decode())

@feat(N, "Info IP / domain")
def _():
    t = ask("IP/domain (kosong = IP sendiri)")
    d = json.loads(get(f"http://ip-api.com/json/{t}").read().decode())
    out("\n".join(f"{k}: {v}" for k, v in d.items()))

@feat(N, "Ping host")
def _():
    h = ask("Host")
    if need("ping"): sh(f"ping -c 4 {h}")

@feat(N, "DNS lookup")
def _():
    h = ask("Domain")
    out("\n".join(sorted({i[4][0] for i in socket.getaddrinfo(h, None)})))

@feat(N, "Reverse DNS")
def _(): out(socket.gethostbyaddr(ask("IP"))[0])

@feat(N, "Cek port terbuka")
def _():
    h, p = ask("Host"), int(ask("Port"))
    s = socket.socket(); s.settimeout(4)
    out("TERBUKA" if s.connect_ex((h, p)) == 0 else "TERTUTUP"); s.close()

@feat(N, "HTTP header")
def _():
    r = get(ask("URL (https://...)"), head=True)
    out(f"Status: {r.status}\n" + "\n".join(f"{k}: {v}" for k, v in r.headers.items()))

@feat(N, "Cek status URL")
def _():
    u = ask("URL"); t = time.time()
    r = get(u, head=True)
    out(f"{r.status} dalam {time.time() - t:.2f} detik")

@feat(N, "Tes kecepatan unduh")
def _():
    t = time.time()
    n = len(get("https://speed.cloudflare.com/__down?bytes=5000000", timeout=30).read())
    d = time.time() - t
    out(f"{n / 1e6:.1f} MB dalam {d:.2f}s = {n * 8 / d / 1e6:.2f} Mbps")

@feat(N, "Info WiFi (termux-api)")
def _():
    if need("termux-wifi-connectioninfo"): sh("termux-wifi-connectioninfo")

@feat(N, "Traceroute")
def _():
    h = ask("Host")
    if need("traceroute"): sh(f"traceroute {h}")

@feat(N, "Cek koneksi internet")
def _():
    try:
        socket.create_connection(("1.1.1.1", 53), 4); out("Online")
    except OSError:
        out("Offline")

@feat(N, "Ambil isi URL (teks)")
def _(): out(get(ask("URL")).read().decode(errors="ignore")[:3000])
