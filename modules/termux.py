# Voxueg modul: Termux
from core.utils import *

TX = "Termux"

@feat(TX, "Tampilkan toast")
def _():
    if need("termux-toast"): sh(f"termux-toast {json.dumps(ask('Pesan'))}")

@feat(TX, "Getarkan HP")
def _():
    if need("termux-vibrate"): sh("termux-vibrate -d 500")

@feat(TX, "Salin ke clipboard")
def _():
    if need("termux-clipboard-set"): sh(f"termux-clipboard-set {json.dumps(ask('Teks'))}")

@feat(TX, "Update paket Termux")
def _(): sh("pkg update -y && pkg upgrade -y")

@feat(TX, "Setup akses penyimpanan")
def _(): sh("termux-setup-storage")
