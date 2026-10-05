from core.utils import *

U = "Utilitas & Online"

@feat(U, "Timer hitung mundur")
def _():
    n = int(ask("Detik"))
    try:
        for i in range(n, 0, -1):
            print(f"\r  {i:>5} detik ", end="", flush=True); time.sleep(1)
    except KeyboardInterrupt:
        print(); return
    print(); out("Waktu habis!")
    if shutil.which("termux-vibrate"): sh("termux-vibrate -d 500")

@feat(U, "Stopwatch")
def _():
    input("  [Enter] mulai"); t = time.time()
    input("  [Enter] berhenti"); out(f"{time.time() - t:.2f} detik")

@feat(U, "Jam digital (10 detik)")
def _():
    try:
        for _ in range(10):
            print(f"\r  {datetime.now():%H:%M:%S}", end="", flush=True); time.sleep(1)
    except KeyboardInterrupt: pass
    print()

@feat(U, "QR code di terminal")
def _():
    t = ask("Teks/URL")
    if need("qrencode"): sh(f"qrencode -t ANSIUTF8 {json.dumps(t)}")

@feat(U, "Cuaca kota")
def _(): out(get("https://wttr.in/" + urllib.parse.quote(ask("Kota")) + "?format=3").read().decode())

@feat(U, "Kurs mata uang")
def _():
    a, f, t = float(ask("Jumlah")), ask("Dari (cth USD)").upper(), ask("Ke (cth IDR)").upper()
    r = json.loads(get("https://open.er-api.com/v6/latest/" + f).read().decode())["rates"]
    out(f"{a:g} {f} = {a * r[t]:,.2f} {t}")

@feat(U, "Jadwal sholat")
def _():
    k = ask("Kota")
    d = json.loads(get("https://api.aladhan.com/v1/timingsByCity?city=" + urllib.parse.quote(k) + "&country=Indonesia&method=11").read().decode())["data"]["timings"]
    out("\n".join(f"{n}: {d[n]}" for n in ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]))

@feat(U, "Info user GitHub")
def _():
    d = json.loads(get("https://api.github.com/users/" + ask("Username")).read().decode())
    out(f"Nama: {d.get('name')}\nBio: {d.get('bio')}\nRepo: {d['public_repos']}\nFollowers: {d['followers']}\nURL: {d['html_url']}")

@feat(U, "Info repo GitHub")
def _():
    d = json.loads(get("https://api.github.com/repos/" + ask("owner/repo")).read().decode())
    out(f"{d['full_name']}\n{d.get('description')}\nBahasa: {d.get('language')}\nStar: {d['stargazers_count']}  Fork: {d['forks_count']}")

@feat(U, "Update Voxueg (git pull)")
def _(): sh(f"git -C {os.path.dirname(os.path.abspath(__file__))} pull")

@feat(U, "Neofetch (info sistem cantik)")
def _():
    if need("neofetch"): sh("neofetch --stdout")

@feat(U, "Tentang Voxueg")
def _(): out(f"{NAME} v{VER}\nDev: {DEV}\nTotal fitur: {len(F)}\nSemua API online yang dipakai gratis tanpa API key.")
