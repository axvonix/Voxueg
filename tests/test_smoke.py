import os, sys, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import modules  # noqa
from core.utils import F

names = [n for _, n, _ in F]
dup = [n for n, c in collections.Counter(names).items() if c > 1]
assert not dup, f"Nama fitur ganda: {dup}"
assert len(F) >= 180, f"Fitur kurang dari 180: {len(F)}"
print(f"OK: {len(F)} fitur, {len(set(c for c, _, _ in F))} kategori, tanpa duplikat")
