"""STL kontrolü: ölçü, manifold, baskı yönünde çıkıntı.

Baskı yönü: STL'nin +Z'si baskıda yukarı. Tabla (z = zmin) üzerindeki yüzler hariç,
normal.z < -0.7072 (45°'den yatık sarkma) ve alanı > 0 olan yüzler raporlanır.

Kullanım: python scripts/stl_check.py dosya.stl [--max-overhang-report 10]
"""
import struct
import sys
from collections import Counter

OVERHANG_LIMIT = -0.7072
BED_EPS = 1e-3


def read_stl(path):
    data = open(path, "rb").read()
    if len(data) >= 84:
        n = struct.unpack_from("<I", data, 80)[0]
        if len(data) == 84 + 50 * n:
            tris = []
            for i in range(n):
                v = struct.unpack_from("<12f", data, 84 + 50 * i)
                tris.append((v[3:6], v[6:9], v[9:12]))
            return tris
    tris, cur = [], []
    for line in data.decode("ascii", "replace").splitlines():
        p = line.split()
        if p and p[0] == "vertex":
            cur.append(tuple(float(x) for x in p[1:4]))
            if len(cur) == 3:
                tris.append(tuple(cur))
                cur = []
    return tris


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    path = sys.argv[1]
    tris = read_stl(path)
    xs = [v[0] for t in tris for v in t]
    ys = [v[1] for t in tris for v in t]
    zs = [v[2] for t in tris for v in t]
    zmin = min(zs)

    key = lambda v: (round(v[0], 4), round(v[1], 4), round(v[2], 4))
    edges = Counter()
    overhang_area, overhang_n, worst = 0.0, 0, 0.0
    for a, b, c in tris:
        ka, kb, kc = key(a), key(b), key(c)
        for e in ((ka, kb), (kb, kc), (kc, ka)):
            edges[tuple(sorted(e))] += 1
        n = cross(sub(b, a), sub(c, a))
        L = (n[0] ** 2 + n[1] ** 2 + n[2] ** 2) ** 0.5
        if L < 1e-12:
            continue
        nz = n[2] / L
        on_bed = max(a[2], b[2], c[2]) - zmin < BED_EPS
        if nz < OVERHANG_LIMIT and not on_bed:
            overhang_area += L / 2
            overhang_n += 1
            worst = min(worst, nz)

    bad_edges = sum(1 for k, c in edges.items() if c != 2)
    print(f"  dosya     : {path}")
    print(f"  üçgen     : {len(tris)}")
    print(f"  ölçü (mm) : {max(xs)-min(xs):.3f} x {max(ys)-min(ys):.3f} x {max(zs)-zmin:.3f}")
    print(f"  manifold  : {'EVET' if bad_edges == 0 else f'HAYIR ({bad_edges} hatalı kenar)'}")
    if overhang_n:
        print(f"  çıkıntı   : {overhang_n} yüz, {overhang_area:.2f} mm², en kötü normal.z = {worst:.3f}")
    else:
        print("  çıkıntı   : yok (tabla dışında > 45° sarkan yüz yok)")


if __name__ == "__main__":
    main()
