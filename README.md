# Voxueg
Tools Termux serba guna, **196 fitur** (termasuk 24 API online tanpa key dan 40 fitur OSINT pasif).
Dev: **Alzeoxyz**

## Instalasi
```bash
pkg install git -y
git clone https://github.com/Alzeoxyz/Voxueg
cd Voxueg
bash install.sh
python voxueg.py
```
Fitur bertanda (termux-api) butuh aplikasi Termux:API.

## Struktur file
```
Voxueg/
├── voxueg.py          # launcher (jalankan ini)
├── install.sh         # installer Termux
├── requirements.txt   # tanpa library pihak ketiga
├── LICENSE
├── README.md
├── core/
│   ├── utils.py       # konstanta, registry fitur, helper (ask, out, sh, get)
│   ├── ui.py          # tema warna, banner besar, kotak, bilah judul
│   └── menu.py        # menu, paginasi, pencarian, pemilih tema
├── modules/           # satu file = satu kategori
│   ├── sistem.py          (11)
│   ├── jaringan.py        (14)
│   ├── teks.py            (30)
│   ├── generator.py       (10)
│   ├── hitung.py          (25)
│   ├── file_tools.py      (9)
│   ├── termux.py          (5)
│   ├── developer.py       (16)
│   ├── utilitas.py        (12)
│   ├── api_online.py      (24)
│   └── osint.py           (40)
└── tests/
    └── test_smoke.py  # cek jumlah fitur & nama ganda
```

## Menambah fitur baru
Buka file kategori di `modules/`, lalu tambahkan:
```python
@feat(S, "Nama fitur")
def _():
    out("Halo dari Voxueg")
```
`S` = konstanta kategori di bagian atas file itu. Fitur otomatis muncul di menu.
Kategori baru: buat `modules/nama.py`, lalu daftarkan di `modules/__init__.py`.

## Catatan etika OSINT
Fitur OSINT bersifat pasif dan memakai data publik. Pakai untuk aset sendiri atau riset berizin.

## Tampilan
Banner VOXUEG bergradasi, menu bernomor `[1]`, halaman kategori berpaginasi (`n`/`p`), dan 6 tema warna (Neon, Hijau, Api, Ungu, Laut, Mono). Tekan `t` di menu utama untuk ganti tema; pilihan tersimpan di `~/.voxueg/config.json`.
