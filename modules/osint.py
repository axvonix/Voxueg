# Voxueg modul: OSINT
from core.utils import *

O = "OSINT"

import urllib.error, ipaddress, mimetypes

UA = {"User-Agent": f"{NAME}/{VER}"}

def req(url, headers=None, data=None, method=None, timeout=15):
    h = dict(UA); h.update(headers or {})
    if data is not None and not isinstance(data, bytes):
        data = json.dumps(data).encode(); h["Content-Type"] = "application/json"
    return urllib.request.urlopen(urllib.request.Request(url, data=data, headers=h, method=method), timeout=timeout)

def JR(url, **k): return json.loads(req(url, **k).read().decode())

def txt(url, **k): return req(url, **k).read().decode(errors="ignore")

def host(s):
    s = s.strip()
    return urllib.parse.urlparse(s if "//" in s else "//" + s).hostname or s

def url_(s): return s.strip() if s.strip().startswith("http") else "https://" + s.strip()

def base(s):
    p = urllib.parse.urlparse(url_(s)); return f"{p.scheme}://{p.netloc}"

def doh(name, typ="A", prov="google"):
    if prov == "google":
        d = JR(f"https://dns.google/resolve?name={q(name)}&type={typ}")
    else:
        d = JR(f"https://cloudflare-dns.com/dns-query?name={q(name)}&type={typ}", headers={"accept": "application/dns-json"})
    return [a["data"] for a in d.get("Answer", [])]

class NoRed(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None

@feat(O, "Catatan etika OSINT")
def _():
    out("Fitur OSINT Voxueg bersifat PASIF dan hanya memakai data publik\n"
        "(DNS, sertifikat, arsip web, registri). Gunakan untuk aset milik sendiri,\n"
        "riset keamanan yang berizin, atau data publik organisasi. Jangan dipakai\n"
        "untuk melacak, melecehkan, atau membuka data pribadi seseorang.")

@feat(O, "DNS semua record")
def _():
    d = host(ask("Domain"))
    for t in ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA", "CAA"]:
        r = doh(d, t)
        out(f"[{t}] " + ("\n     ".join(r) if r else "-"))

@feat(O, "DNS MX (server email)")
def _(): out("\n".join(doh(host(ask("Domain")), "MX")) or "-")

@feat(O, "DNS NS (nameserver)")
def _(): out("\n".join(doh(host(ask("Domain")), "NS")) or "-")

@feat(O, "DNS TXT")
def _(): out("\n".join(doh(host(ask("Domain")), "TXT")) or "-")

@feat(O, "DNS CAA")
def _(): out("\n".join(doh(host(ask("Domain")), "CAA")) or "Tidak ada CAA")

@feat(O, "Cek SPF & DMARC")
def _():
    d = host(ask("Domain"))
    spf = [x for x in doh(d, "TXT") if "v=spf1" in x]
    dm = [x for x in doh("_dmarc." + d, "TXT") if "v=DMARC1" in x]
    out("SPF  : " + (spf[0] if spf else "TIDAK ADA") + "\nDMARC: " + (dm[0] if dm else "TIDAK ADA"))

@feat(O, "Bandingkan DNS Google vs Cloudflare")
def _():
    d = host(ask("Domain"))
    a, b = sorted(doh(d, "A")), sorted(doh(d, "A", "cf"))
    out(f"Google    : {a}\nCloudflare: {b}\n" + ("Sama" if a == b else "BEDA (cek propagasi/CDN)"))

@feat(O, "Subdomain pasif (crt.sh)")
def _():
    d = host(ask("Domain"))
    s = set()
    for e in JR(f"https://crt.sh/?q=%25.{q(d)}&output=json", timeout=45):
        for n in e["name_value"].split("\n"): s.add(n.lower().lstrip("*."))
    out(f"{len(s)} subdomain unik (dari Certificate Transparency)\n" + "\n".join(sorted(s)[:100]))

@feat(O, "Info sertifikat SSL + SAN")
def _():
    import ssl
    h = host(ask("Domain"))
    with socket.create_connection((h, 443), 8) as s:
        with ssl.create_default_context().wrap_socket(s, server_hostname=h) as ss: c = ss.getpeercert()
    sj, isr = dict(x[0] for x in c["subject"]), dict(x[0] for x in c["issuer"])
    san = [v for _, v in c.get("subjectAltName", [])]
    out(f"CN     : {sj.get('commonName')}\nPenerbit: {isr.get('organizationName')}\nMulai  : {c['notBefore']}\n"
        f"Selesai: {c['notAfter']}\nSAN ({len(san)}):\n" + "\n".join(san[:50]))

@feat(O, "Versi TLS & cipher server")
def _():
    import ssl
    h = host(ask("Domain"))
    with socket.create_connection((h, 443), 8) as s:
        with ssl.create_default_context().wrap_socket(s, server_hostname=h) as ss:
            out(f"TLS   : {ss.version()}\nCipher: {ss.cipher()[0]} ({ss.cipher()[2]} bit)")

@feat(O, "Wayback: snapshot terdekat")
def _():
    s = JR("https://archive.org/wayback/available?url=" + q(ask("URL/domain")))["archived_snapshots"].get("closest")
    out(f"{s['url']}\nWaktu: {s['timestamp']}" if s else "Tidak ada arsip.")

@feat(O, "Wayback: daftar snapshot (CDX)")
def _():
    rows = JR("https://web.archive.org/cdx/search/cdx?output=json&limit=20&collapse=digest&fl=timestamp,statuscode,original&url=" + q(ask("URL/domain")), timeout=40)
    out("\n".join(f"{r[0]}  {r[1]}  {r[2]}" for r in rows[1:]) or "Tidak ada arsip.")

@feat(O, "Deteksi teknologi web")
def _():
    r = req(url_(ask("URL")))
    body = r.read(300000).decode(errors="ignore")
    hd = {k.lower(): v for k, v in r.headers.items()}
    hasil = [f"{k}: {hd[k]}" for k in ("server", "x-powered-by", "x-generator", "via", "x-served-by") if k in hd]
    if "cf-ray" in hd: hasil.append("CDN: Cloudflare")
    m = re.search(r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']([^"\']+)', body, re.I)
    if m: hasil.append("generator: " + m.group(1))
    sig = {"WordPress": "wp-content", "Joomla": "/media/jui/", "Drupal": "drupal.settings", "Shopify": "cdn.shopify.com",
           "Wix": "wixstatic.com", "Next.js": "/_next/", "Angular": "ng-version", "jQuery": "jquery",
           "Bootstrap": "bootstrap", "Google Analytics": "google-analytics.com", "Tag Manager": "googletagmanager.com"}
    low = body.lower()
    hasil += [f"terdeteksi: {k}" for k, v in sig.items() if v in low]
    out("\n".join(hasil) or "Tidak ada petunjuk (hasil heuristik)")

@feat(O, "Lihat robots.txt")
def _(): out(txt(base(ask("Domain/URL")) + "/robots.txt")[:2500])

@feat(O, "Lihat sitemap.xml")
def _(): out(txt(base(ask("Domain/URL")) + "/sitemap.xml")[:2500])

@feat(O, "Lihat security.txt")
def _(): out(txt(base(ask("Domain/URL")) + "/.well-known/security.txt")[:2000])

@feat(O, "Audit header keamanan")
def _():
    r = req(url_(ask("URL")))
    hd = {k.lower() for k in r.headers.keys()}
    cek = ["strict-transport-security", "content-security-policy", "x-frame-options",
           "x-content-type-options", "referrer-policy", "permissions-policy"]
    out("\n".join(f"{'ADA   ' if c in hd else 'TIDAK '} {c}" for c in cek))

@feat(O, "Lacak rantai redirect")
def _():
    op, u = urllib.request.build_opener(NoRed), url_(ask("URL"))
    for i in range(1, 11):
        try:
            r = op.open(urllib.request.Request(u, headers=UA), timeout=15)
            out(f"{i}. {r.status} {u}"); break
        except urllib.error.HTTPError as e:
            out(f"{i}. {e.code} {u}")
            loc = e.headers.get("Location")
            if e.code in (301, 302, 303, 307, 308) and loc: u = urllib.parse.urljoin(u, loc)
            else: break

@feat(O, "Ekstrak link halaman")
def _():
    u = url_(ask("URL"))
    body = txt(u)
    ls = sorted({urllib.parse.urljoin(u, x) for x in re.findall(r'href=["\']([^"\'#]+)', body, re.I)})
    dom = urllib.parse.urlparse(u).netloc
    ext = [x for x in ls if urllib.parse.urlparse(x).netloc != dom]
    out(f"Total {len(ls)} link ({len(ext)} eksternal)\n" + "\n".join(ls[:60]))

@feat(O, "Metode HTTP yang diizinkan")
def _():
    try:
        r = req(url_(ask("URL")), method="OPTIONS"); out(r.headers.get("Allow", "Header Allow tidak ada"))
    except urllib.error.HTTPError as e:
        out(e.headers.get("Allow", f"Server menolak OPTIONS ({e.code})"))

@feat(O, "Cek flag cookie")
def _():
    r = req(url_(ask("URL")))
    cs = r.headers.get_all("Set-Cookie") or []
    for c in cs:
        l = c.lower()
        out(f"{c.split('=')[0]}: Secure={'secure' in l} HttpOnly={'httponly' in l} SameSite={'samesite' in l}")
    if not cs: out("Tidak ada Set-Cookie")

@feat(O, "Waktu respons (TTFB)")
def _():
    t = time.time(); r = req(url_(ask("URL"))); r.read(1); a = time.time() - t
    n = 1 + len(r.read()); b = time.time() - t
    out(f"TTFB : {a * 1000:.0f} ms\nTotal: {b * 1000:.0f} ms\nUkuran: {n / 1024:.1f} KB")

@feat(O, "ASN & prefix IP (RIPEstat)")
def _():
    d = JR("https://stat.ripe.net/data/prefix-overview/data.json?resource=" + q(ask("IP"))) ["data"]
    out(f"Prefix: {d.get('resource')}\n" + "\n".join(f"AS{a['asn']}: {a['holder']}" for a in d.get("asns", [])))

@feat(O, "Whois IP (RDAP)")
def _():
    d = JR("https://rdap.org/ip/" + q(ask("IP")))
    out(f"Nama: {d.get('name')}\nRentang: {d.get('startAddress')} - {d.get('endAddress')}\nNegara: {d.get('country')}\nTipe: {d.get('type')}")

@feat(O, "Reverse IP (domain di IP yang sama)")
def _(): out(txt("https://api.hackertarget.com/reverseiplookup/?q=" + q(ask("IP/domain")))[:2500])

@feat(O, "Cek IP publik/privat")
def _():
    i = ipaddress.ip_address(ask("IP"))
    out(f"IPv{i.version}\nGlobal: {i.is_global}\nPrivat: {i.is_private}\nLoopback: {i.is_loopback}\nMulticast: {i.is_multicast}")

@feat(O, "Kalkulator CIDR")
def _():
    n = ipaddress.ip_network(ask("CIDR (cth 192.168.1.0/24)"), strict=False)
    h = list(n.hosts()) if n.num_addresses <= 65536 else None
    out(f"Network: {n.network_address}\nBroadcast: {n.broadcast_address}\nNetmask: {n.netmask}\nTotal alamat: {n.num_addresses}"
        + (f"\nHost: {h[0]} - {h[-1]}" if h else ""))

@feat(O, "Umur domain (RDAP)")
def _():
    d = JR("https://rdap.org/domain/" + q(host(ask("Domain"))))
    for e in d.get("events", []):
        if e["eventAction"] == "registration":
            t = datetime.strptime(e["eventDate"][:10], "%Y-%m-%d").date()
            out(f"Terdaftar: {t}\nUmur: {(date.today() - t).days / 365.25:.1f} tahun"); return
    out("Tanggal registrasi tidak tersedia")

@feat(O, "Cek ketersediaan domain")
def _():
    try:
        req("https://rdap.org/domain/" + q(host(ask("Domain")))); out("Sudah terdaftar")
    except urllib.error.HTTPError as e:
        out("Kemungkinan tersedia (RDAP 404)" if e.code == 404 else f"Tidak pasti (HTTP {e.code})")

@feat(O, "Detail CVE (NVD)")
def _():
    v = JR("https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=" + q(ask("ID CVE (CVE-2021-44228)").upper()))["vulnerabilities"]
    if not v: out("Tidak ditemukan"); return
    c = v[0]["cve"]
    desk = next((x["value"] for x in c["descriptions"] if x["lang"] == "en"), "-")
    sk = c.get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {}).get("baseScore", "-")
    out(f"{c['id']}\nDiterbitkan: {c['published'][:10]}\nCVSS v3.1: {sk}\n{desk[:900]}")

@feat(O, "Cari CVE kata kunci")
def _():
    v = JR("https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=10&keywordSearch=" + q(ask("Kata kunci")))["vulnerabilities"]
    out("\n".join(f"{x['cve']['id']}  {x['cve']['published'][:10]}" for x in v) or "Tidak ada hasil")

@feat(O, "Cek kerentanan paket (OSV)")
def _():
    n, e, v = ask("Nama paket"), ask("Ekosistem (PyPI/npm/Go/Maven)"), ask("Versi")
    r = JR("https://api.osv.dev/v1/query", data={"package": {"name": n, "ecosystem": e}, "version": v}).get("vulns", [])
    out(f"{len(r)} kerentanan\n" + "\n".join(f"{x['id']}: {x.get('summary', '-')[:90]}" for x in r[:15]))

@feat(O, "Repo publik organisasi GitHub")
def _():
    r = JR("https://api.github.com/orgs/" + q(ask("Nama organisasi")) + "/repos?per_page=30&sort=updated")
    out("\n".join(f"{x['name']}  *{x['stargazers_count']}  {x.get('language')}" for x in r) or "Kosong")

@feat(O, "Rilis terbaru repo GitHub")
def _():
    d = JR("https://api.github.com/repos/" + ask("owner/repo") + "/releases/latest")
    out(f"{d.get('name') or d['tag_name']}\nTag: {d['tag_name']}\nTanggal: {d['published_at'][:10]}")

@feat(O, "Komposisi bahasa repo GitHub")
def _():
    d = JR("https://api.github.com/repos/" + ask("owner/repo") + "/languages")
    t = sum(d.values()) or 1
    out("\n".join(f"{k}: {v * 100 / t:.1f}%" for k, v in d.items()))

@feat(O, "Identifikasi jenis hash")
def _():
    h = ask("Hash").strip()
    if h.startswith(("$2a$", "$2b$", "$2y$")): out("bcrypt"); return
    for p, n in [("$argon2", "Argon2"), ("$6$", "sha512crypt"), ("$5$", "sha256crypt"), ("$1$", "md5crypt")]:
        if h.startswith(p): out(n); return
    if re.fullmatch(r"[0-9a-fA-F]+", h):
        out({8: "CRC32/Adler32", 32: "MD5 / NTLM", 40: "SHA-1", 56: "SHA-224", 64: "SHA-256 / SHA3-256",
             96: "SHA-384", 128: "SHA-512 / SHA3-512"}.get(len(h), f"Tidak dikenal (panjang {len(h)})"))
    else: out("Format tidak dikenali")

@feat(O, "Decode JWT (tanpa verifikasi)")
def _():
    def dec(s): return json.loads(base64.urlsafe_b64decode(s + "=" * (-len(s) % 4)))
    h, p, *_r = ask("Token JWT").split(".")
    out("Header: " + json.dumps(dec(h)) + "\nPayload: " + json.dumps(dec(p), indent=2))

@feat(O, "Parse komponen URL")
def _():
    p = urllib.parse.urlparse(ask("URL"))
    out(f"Skema: {p.scheme}\nHost: {p.hostname}\nPort: {p.port}\nPath: {p.path}\nQuery: {urllib.parse.parse_qs(p.query)}\nFragment: {p.fragment}")

@feat(O, "Metadata file lokal")
def _():
    f = ask("Path file"); s = os.stat(f)
    out(f"Ukuran: {s.st_size} byte\nTipe: {mimetypes.guess_type(f)[0] or '?'}\nDiubah: {datetime.fromtimestamp(s.st_mtime)}\n"
        f"Izin: {oct(s.st_mode)[-3:]}")
