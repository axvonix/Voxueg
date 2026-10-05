# Voxueg modul: Sistem
from core.utils import *

S = "Sistem"

@feat(S, "Info perangkat")
def _():
    out(f"OS      : {platform.system()} {platform.release()}\nArch    : {platform.machine()}\nHost    : {socket.gethostname()}\nPython  : {platform.python_version()}")

@feat(S, "Uptime")
def _(): sh("uptime")

@feat(S, "Memori (RAM)")
def _(): sh("free -h")

@feat(S, "Penyimpanan (disk)")
def _(): sh("df -h $HOME")

@feat(S, "Info CPU")
def _():
    out(f"Jumlah core: {os.cpu_count()}")
    sh("grep -m1 -i 'model name\\|Hardware' /proc/cpuinfo")

@feat(S, "Status baterai (termux-api)")
def _():
    if need("termux-battery-status"): sh("termux-battery-status")

@feat(S, "Daftar proses")
def _(): sh("ps -e | head -30")

@feat(S, "Variabel lingkungan")
def _(): out("\n".join(f"{k}={v}" for k, v in sorted(os.environ.items())[:40]))

@feat(S, "Tanggal & waktu")
def _(): out(datetime.now().strftime("%A, %d %B %Y  %H:%M:%S"))

@feat(S, "Kalender bulan ini")
def _(): out(calendar.month(date.today().year, date.today().month))

@feat(S, "Info Termux")
def _(): out(f"HOME  : {os.environ.get('HOME')}\nPREFIX: {os.environ.get('PREFIX')}\nSHELL : {os.environ.get('SHELL')}")
