#!/usr/bin/env python3
"""
verify_hc18.py (v2) - pengecekan independen untuk hasil P4 (HC18).
Jalankan dari root proyek skripsi:
    python scripts/verify_hc18.py --data data/hc18 --splits splits/hc18_group5fold_seed42.csv | tee research-notes/hc18-P4c-verify.txt
Hanya membaca data. Tempel SELURUH output mentah ke chat untuk diaudit.
Perubahan dari v1: group di file split dihitung ulang dari nama file (tidak percaya kolom 'group'),
kolom nama file bisa 'filename' atau 'file', floor dihitung di beberapa resolusi dan dua mode resize,
dan kasus terburuk dicantumkan.
"""
import argparse, math, os, sys
import numpy as np
import pandas as pd


def ramanujan(a, b):
    return math.pi * (3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b)))


def fit_hc_mm(mask, px):
    import cv2
    cs, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not cs:
        return None
    c = max(cs, key=cv2.contourArea)
    if len(c) < 5:
        return None
    (_, _), (w, h), _ = cv2.fitEllipse(c)
    return ramanujan(w / 2, h / 2) * px


def stats(name, v):
    v = np.asarray([x for x in v if x is not None])
    if len(v):
        print(f"{name}: n={len(v)} MAE={v.mean():.4f} mm | median={np.median(v):.4f} | p95={np.percentile(v, 95):.4f} | max={v.max():.4f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/hc18")
    ap.add_argument("--splits", default="splits/hc18_group5fold_seed42.csv")
    ap.add_argument("--scales", default="0.64,0.48,0.32", help="skala resize untuk simulasi resolusi input model")
    ap.add_argument("--max-floor", type=int, default=0, help="batasi jumlah citra untuk floor (0 = semua)")
    a = ap.parse_args()
    scales = [float(s) for s in a.scales.split(",")]

    tr_csv = os.path.join(a.data, "training_set_pixel_size_and_HC.csv")
    te_csv = os.path.join(a.data, "test_set_pixel_size.csv")
    df = pd.read_csv(tr_csv)
    df.columns = ["filename", "px", "hc"]
    df["group"] = df.filename.str.extract(r"^(\d+)_")[0].astype(int)

    print("=== A. STRUKTUR GRUP ===")
    print("citra:", len(df), "| grup unik:", df.group.nunique())
    print("distribusi ukuran grup:\n", df.groupby("group").size().value_counts().sort_index().to_string())

    print("\n=== B. RENTANG PIXEL SIZE (paper HC18 menyebut 0.052-0.326 mm) ===")
    print("train min/max:", df.px.min(), df.px.max())
    print(df.loc[[df.px.idxmin(), df.px.idxmax()]].to_string())
    if os.path.exists(te_csv):
        te = pd.read_csv(te_csv)
        te.columns = ["filename", "px"]
        print("test  min/max:", te.px.min(), te.px.max())
    print("citra train di luar [0.052, 0.326]:", int(((df.px < 0.052) | (df.px > 0.326)).sum()))
    print("kuantil pixel size train (0,5,25,50,75,95,100):", np.percentile(df.px, [0, 5, 25, 50, 75, 95, 100]).round(4).tolist())

    print("\n=== C. KONSISTENSI DALAM GRUP (apakah satu prefiks = satu janin pada waktu yang sama?) ===")
    multi = df.groupby("group").filter(lambda x: len(x) > 1)
    gm = multi.groupby("group")
    print("grup multi-citra:", gm.ngroups)
    print("  proporsi dengan pixel size identik:", round(float(gm.px.nunique().eq(1).mean()), 4))
    cv = gm.hc.std() / gm.hc.mean()
    print("  CV HC dalam grup (std/mean):\n", cv.describe().round(4).to_string())
    print("  CV HC seluruh data (pembanding):", round(float(df.hc.std() / df.hc.mean()), 4))
    out = cv[cv > 0.08].index.tolist()
    print(f"  grup dengan CV HC > 0.08 (perlu dilihat manual): {len(out)}")
    if out:
        print(multi[multi.group.isin(out)].sort_values(["group", "filename"]).to_string(index=False))

    print("\n=== D. FOLD & KEBOCORAN (group dihitung ulang dari nama file) ===")
    if os.path.exists(a.splits):
        f = pd.read_csv(a.splits)
        print("kolom:", f.columns.tolist(), "| baris:", len(f))
        fn = next((c for c in ("filename", "file", "image") if c in f.columns), None)
        if fn is None or "fold" not in f.columns:
            print("TIDAK ADA kolom nama file atau fold, pengecekan dilewati")
        else:
            f["group_derived"] = f[fn].str.extract(r"^(\d+)_")[0].astype(int)
            if "group" in f.columns:
                print("baris dengan kolom 'group' != group dari nama file:", int((f.group != f.group_derived).sum()))
            print("nama file duplikat di file split:", int(f[fn].duplicated().sum()))
            print("citra di CSV tapi tidak ada di split:", len(set(df.filename) - set(f[fn])),
                  "| citra di split tapi tidak ada di CSV:", len(set(f[fn]) - set(df.filename)))
            lk = f.groupby("group_derived").fold.nunique()
            print("grup (dari nama file) yang muncul di >1 fold:", int((lk > 1).sum()))
            print("ukuran fold:\n", f.fold.value_counts().sort_index().to_string())
            m = f.merge(df[["filename", "hc", "px"]], left_on=fn, right_on="filename", how="left", suffixes=("", "_csv"))
            print("HC per fold dari CSV resmi (mean/min/max):\n",
                  m.groupby("fold").hc.agg(["mean", "min", "max"]).round(2).to_string())
            for col in ("hc_mm", "hc"):
                if col in f.columns:
                    print(f"selisih maksimum kolom '{col}' di split vs CSV resmi:", float((m[col] - m["hc"]).abs().max()) if col != "hc" else "n/a")
    else:
        print("file splits tidak ditemukan:", a.splits)

    print("\n=== E. FLOOR PER PIPELINE: mask terisi -> (resize) -> kontur -> fitEllipse -> Ramanujan, vs HC di CSV ===")
    try:
        import cv2
    except Exception as e:
        print("cv2 tidak tersedia, lewati:", e)
        return
    sub = df if a.max_floor <= 0 else df.head(a.max_floor)
    native, per_img = [], []
    near = {s: [] for s in scales}
    soft = {s: [] for s in scales}
    fail = 0
    for r in sub.itertuples():
        ann = os.path.join(a.data, "training_set", r.filename.replace(".png", "_Annotation.png"))
        if not os.path.exists(ann):
            fail += 1
            continue
        im = cv2.imread(ann, cv2.IMREAD_GRAYSCALE)
        pts = cv2.findNonZero((im > 0).astype(np.uint8))
        if pts is None or len(pts) < 5:
            fail += 1
            continue
        (cx, cy), (w, h), ang = cv2.fitEllipse(pts)
        H, W = im.shape
        mask = np.zeros_like(im, dtype=np.uint8)
        cv2.ellipse(mask, ((cx, cy), (w, h), ang), 255, -1)
        ys, xs = np.nonzero(im)
        border = bool(xs.min() <= 0 or ys.min() <= 0 or xs.max() >= W - 1 or ys.max() >= H - 1)
        hc0 = fit_hc_mm(mask, r.px)
        e0 = None if hc0 is None else abs(hc0 - r.hc)
        native.append(e0)
        per_img.append((r.filename, r.px, r.hc, e0, border))
        for s in scales:
            small = cv2.resize(mask, None, fx=s, fy=s, interpolation=cv2.INTER_NEAREST)
            h1 = fit_hc_mm(small, r.px / s)
            near[s].append(None if h1 is None else abs(h1 - r.hc))
            sm = cv2.resize((mask > 0).astype(np.float32), None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
            up = cv2.resize(sm, (W, H), interpolation=cv2.INTER_LINEAR)
            h2 = fit_hc_mm(((up > 0.5).astype(np.uint8)) * 255, r.px)
            soft[s].append(None if h2 is None else abs(h2 - r.hc))
    stats("native (mask terisi, resolusi penuh)", native)
    for s in scales:
        stats(f"x{s}  nearest (mask keras di resolusi rendah, kontur diskret)", near[s])
        stats(f"x{s}  soft    (area-resize lalu bilinear-upsample lalu ambang 0.5)", soft[s])
    pi = pd.DataFrame(per_img, columns=["filename", "px", "hc_csv", "err_native_mm", "touches_border"]).dropna()
    print("\n10 kasus terburuk (native):")
    print(pi.sort_values("err_native_mm", ascending=False).head(10).to_string(index=False))
    print("\nMAE native per kuartil pixel size:")
    pi["px_q"] = pd.qcut(pi.px, 4)
    print(pi.groupby("px_q", observed=True).err_native_mm.agg(["count", "mean", "max"]).round(4).to_string())
    print("\nanotasi menyentuh tepi:", int(pi.touches_border.sum()), "| MAE native pada kasus tepi:",
          round(float(pi[pi.touches_border].err_native_mm.mean()), 4) if pi.touches_border.any() else "n/a",
          "| anotasi tidak terbaca:", fail)


if __name__ == "__main__":
    sys.exit(main())
