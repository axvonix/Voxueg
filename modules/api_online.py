# Voxueg modul: API Online
from core.utils import *

A = "API Online"

@feat(A, "Info negara")
def _():
    d = J("https://restcountries.com/v3.1/name/" + q(ask("Nama negara")))[0]
    out(f"{d['name']['common']}\nIbu kota: {', '.join(d.get('capital', ['-']))}\nBenua: {d['region']}\n"
        f"Populasi: {d['population']:,}\nMata uang: {', '.join(d.get('currencies', {}).keys())}\n"
        f"Bahasa: {', '.join(d.get('languages', {}).values())}")

@feat(A, "Cuaca detail (Open-Meteo)")
def _():
    g = J("https://geocoding-api.open-meteo.com/v1/search?count=1&name=" + q(ask("Kota")))["results"][0]
    w = J(f"https://api.open-meteo.com/v1/forecast?latitude={g['latitude']}&longitude={g['longitude']}"
          "&current_weather=true&daily=temperature_2m_max,temperature_2m_min&timezone=auto")
    c, d = w["current_weather"], w["daily"]
    out(f"{g['name']}, {g.get('country', '')}\nSekarang: {c['temperature']}°C, angin {c['windspeed']} km/j\n"
        f"Hari ini: {d['temperature_2m_min'][0]}°C - {d['temperature_2m_max'][0]}°C")

@feat(A, "Gempa terbaru BMKG")
def _():
    g = J("https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json")["Infogempa"]["gempa"]
    out(f"{g['Tanggal']} {g['Jam']}\nMagnitudo: {g['Magnitude']}\nKedalaman: {g['Kedalaman']}\n"
        f"Wilayah: {g['Wilayah']}\nPotensi: {g['Potensi']}")

@feat(A, "Hari libur nasional")
def _():
    y = ask("Tahun (default sekarang)") or str(date.today().year)
    out("\n".join(f"{h['date']}  {h['localName']}" for h in J(f"https://date.nager.at/api/v3/PublicHolidays/{y}/ID")))

@feat(A, "Cek paket npm")
def _():
    d = J("https://registry.npmjs.org/" + q(ask("Nama paket")) + "/latest")
    out(f"{d['name']} v{d['version']}\n{d.get('description', '')}\nLisensi: {d.get('license', '-')}")

@feat(A, "Cek paket PyPI")
def _():
    i = J("https://pypi.org/pypi/" + q(ask("Nama paket")) + "/json")["info"]
    out(f"{i['name']} v{i['version']}\n{i.get('summary', '')}\nPython: {i.get('requires_python', '-')}")

@feat(A, "Waktu dunia")
def _():
    d = J("https://worldtimeapi.org/api/timezone/" + (ask("Zona (default Asia/Jakarta)") or "Asia/Jakarta"))
    out(f"{d['timezone']}\n{d['datetime'][:19].replace('T', ' ')}  (UTC{d['utc_offset']})")

@feat(A, "Posisi ISS sekarang")
def _():
    p = J("http://api.open-notify.org/iss-now.json")["iss_position"]
    out(f"Lat: {p['latitude']}\nLon: {p['longitude']}")

@feat(A, "Info Pokemon")
def _():
    d = J("https://pokeapi.co/api/v2/pokemon/" + q(ask("Nama/ID").lower()))
    out(f"{d['name'].title()} (#{d['id']})\nTipe: {', '.join(t['type']['name'] for t in d['types'])}\n"
        f"Tinggi: {d['height'] / 10} m  Berat: {d['weight'] / 10} kg\n"
        f"Ability: {', '.join(a['ability']['name'] for a in d['abilities'])}")

@feat(A, "Info registrasi domain (RDAP)")
def _():
    d = J("https://rdap.org/domain/" + q(ask("Domain")))
    ev = "\n".join(f"{e['eventAction']}: {e['eventDate'][:10]}" for e in d.get("events", []))
    out(f"{d.get('ldhName')}\nStatus: {', '.join(d.get('status', []))}\n{ev}")

@feat(A, "Cek masa berlaku SSL")
def _():
    import ssl
    h = ask("Domain")
    with socket.create_connection((h, 443), 8) as s:
        with ssl.create_default_context().wrap_socket(s, server_hostname=h) as ss:
            c = ss.getpeercert()
    sisa = (ssl.cert_time_to_seconds(c["notAfter"]) - time.time()) / 86400
    out(f"Berlaku sampai: {c['notAfter']}\nSisa: {sisa:.0f} hari")

@feat(A, "Pendekkan URL (is.gd)")
def _(): out(get("https://is.gd/create.php?format=simple&url=" + q(ask("URL panjang"))).read().decode())

@feat(A, "Kuis trivia")
def _():
    import html
    d = J("https://opentdb.com/api.php?amount=1&type=multiple")["results"][0]
    op = [html.unescape(x) for x in d["incorrect_answers"] + [d["correct_answer"]]]
    random.shuffle(op)
    out(html.unescape(d["question"]) + "\n" + "\n".join(f"{i}. {o}" for i, o in enumerate(op, 1)))
    s = ask("Jawaban (nomor)")
    ok = s.isdigit() and 1 <= int(s) <= len(op) and op[int(s) - 1] == html.unescape(d["correct_answer"])
    out(("BENAR!" if ok else "Salah.") + f" Jawaban: {html.unescape(d['correct_answer'])}")

@feat(A, "Terjemahan (MyMemory)")
def _():
    t, lp = ask("Teks"), ask("Arah (cth en|id, id|en)") or "en|id"
    out(J(f"https://api.mymemory.translated.net/get?q={q(t)}&langpair={q(lp)}")["responseData"]["translatedText"])

@feat(A, "Kamus bahasa Inggris")
def _():
    d = J("https://api.dictionaryapi.dev/api/v2/entries/en/" + q(ask("Kata")))[0]
    for m in d["meanings"][:3]:
        out(f"({m['partOfSpeech']}) {m['definitions'][0]['definition']}")

@feat(A, "Harga crypto (CoinGecko)")
def _():
    i = ask("ID koin (cth bitcoin, ethereum)").lower()
    d = J(f"https://api.coingecko.com/api/v3/simple/price?ids={q(i)}&vs_currencies=usd,idr")[i]
    out(f"USD: {d['usd']:,}\nIDR: {d['idr']:,}")

@feat(A, "Ringkasan Wikipedia")
def _():
    d = J("https://id.wikipedia.org/api/rest_v1/page/summary/" + q(ask("Judul artikel").replace(" ", "_")))
    out(f"{d['title']}\n{d['extract'][:1200]}")

@feat(A, "Tebak umur dari nama")
def _():
    d = J("https://api.agify.io?name=" + q(ask("Nama depan")))
    out(f"Perkiraan umur: {d['age']} (dari {d['count']} data)")

@feat(A, "Tebak gender dari nama")
def _():
    d = J("https://api.genderize.io?name=" + q(ask("Nama depan")))
    out(f"{d['gender']} (peluang {d['probability']})")

@feat(A, "Tebak asal negara dari nama")
def _():
    d = J("https://api.nationalize.io?name=" + q(ask("Nama depan")))
    out("\n".join(f"{c['country_id']}: {c['probability']:.0%}" for c in d["country"][:5]))

@feat(A, "Fakta kucing")
def _(): out(J("https://catfact.ninja/fact")["fact"])

@feat(A, "Lelucon acak")
def _():
    d = J("https://official-joke-api.appspot.com/random_joke")
    out(f"{d['setup']}\n{d['punchline']}")

@feat(A, "Kutipan motivasi")
def _():
    d = J("https://zenquotes.io/api/random")[0]
    out(f"\"{d['q']}\"\n- {d['a']}")

@feat(A, "Saran acak")
def _(): out(J("https://api.adviceslip.com/advice")["slip"]["advice"])
