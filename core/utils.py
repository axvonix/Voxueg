# Voxueg core: konstanta, registry fitur, dan helper umum | Dev: Alzeoxyz
import os, sys, time, json, uuid, random, string, hashlib, base64, socket
import platform, shutil, subprocess, urllib.request, urllib.parse, binascii
import math, codecs, re, zipfile, ast, operator, calendar
from datetime import datetime, date

NAME, DEV, VER = "Voxueg", "Alzeoxyz", "4.2.1"

C = {"r": "\033[91m", "g": "\033[92m", "y": "\033[93m", "c": "\033[96m", "b": "\033[1m", "0": "\033[0m"}

NOTES = os.path.expanduser("~/.voxueg/catatan.txt")

F = []

def feat(cat, name):
    def d(f):
        F.append((cat, name, f))
        return f
    return d

def ask(p):
    return input(f"  {C['c']}{p}{C['0']}: ").strip()

def out(x):
    print("  " + str(x).replace("\n", "\n  "))

def sh(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=90)
        out((r.stdout + r.stderr).strip() or "(kosong)")
    except Exception as e:
        out(f"Error: {e}")

def need(b):
    if shutil.which(b):
        return True
    out(f"Butuh '{b}'. Pasang dengan: pkg install {b}")
    return False

def get(url, head=False, timeout=15):
    req = urllib.request.Request(url, method="HEAD" if head else "GET",
                                 headers={"User-Agent": f"{NAME}/{VER}"})
    return urllib.request.urlopen(req, timeout=timeout)

def safe(fn):
    def w():
        try:
            fn()
        except Exception as e:
            out(f"{C['r']}Error: {e}{C['0']}")
    w.__doc__ = fn.__doc__
    return w

def J(url):
    return json.loads(get(url).read().decode())

def q(s):
    return urllib.parse.quote(s)
