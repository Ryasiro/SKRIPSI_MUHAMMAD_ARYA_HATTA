#!/usr/bin/env python3
"""lint_note.py - pemeriksa format dan konsistensi internal untuk catatan riset (Kontrak Output v2).

Pemakaian:
    python scripts/lint_note.py research-notes/<berkas>.md
    python scripts/lint_note.py research-notes/hc18-P4-inspeksi-data.md \
        --hc-csv data/hc18/training_set_pixel_size_and_HC.csv

Yang diperiksa (semuanya mekanis, tanpa membuka sumber apa pun):
  - frontmatter dan bagian wajib;
  - nilai kolom `hasil` di Log akses dan `status` di Tabel klaim;
  - status VERIFIED-* harus punya URL, kutipan (maks 15 kata), dan URL itu tercatat di Log akses
    dengan hasil yang sesuai (PRIMARY wajib `dibuka-penuh`);
  - klaim negatif tidak boleh berstatus VERIFIED-*;
  - tanda `~` atau perkiraan di Search log;
  - kalimat menilai diri sendiri ("LOLOS", "siap lanjut", dst.) dan DOI terlarang;
  - opsional --hc-csv: nama berkas citra latih dan nilai HC yang disebut di teks dicocokkan ke CSV resmi.

Keluaran ini BUKAN penilaian kebenaran isi. Kode keluar 1 jika ada ERROR, 0 jika tidak.
Skrip hanya membaca berkas; tidak mengubah apa pun.
"""
import argparse
import csv
import re
import sys
from pathlib import Path

ACCESS_OK = {"dibuka-penuh", "hanya-abstrak", "diblokir", "paywall", "error", "tidak-dicoba"}
STATUS_OK = {"VERIFIED-PRIMARY", "VERIFIED-SECONDARY", "NOT-OPENED", "NOT-FOUND-IN-SEARCH"}
NOTE_STATUS_OK = {"draft", "diverifikasi-agent", "diaudit-manusia"}
FORBIDDEN_DOI = ["10.1002/uog.19029"]
SELF_CERT = re.compile(
    r"\bLOLOS\b|siap\s+(?:lanjut|dipakai|digunakan)|lanjut\s+ke\s+P5|"
    r"terverifikasi\s+(?:lengkap|seluruhnya|semua)|semua\s+(?:klaim|sumber|referensi)\s+(?:telah\s+)?(?:terverifikasi|diverifikasi)",
    re.I,
)
NEGATIVE_CLAIM = re.compile(
    r"belum\s+ditemukan|tidak\s+ada\s+(?:studi|paper|makalah|penelitian)|belum\s+ada\s+(?:studi|paper|makalah|penelitian)|"
    r"no\s+(?:prior\s+)?stud(?:y|ies)|first\s+to\b|satu-satunya|pertama\s+kali",
    re.I,
)
APPROX = re.compile(r"[~≈±]|sekitar|kira-kira|approx", re.I)
SEP_ROW = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
HC_FILE = re.compile(r"(?<!\d)(\d{3}_(?:\d)?HC)(?:_Annotation)?\.png")


class Report:
    def __init__(self):
        self.items = []

    def add(self, level, line, msg):
        self.items.append((level, line, msg))

    def count(self, level):
        return sum(1 for x in self.items if x[0] == level)


def strip_md(s):
    s = s.strip()
    s = re.sub(r"[`*_]", "", s)
    return s.strip()


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def parse_frontmatter(lines):
    if not lines or lines[0].strip() != "---":
        return None, 0
    fm = {}
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return fm, i + 1
        m = re.match(r"^([A-Za-z0-9_\-]+)\s*:\s*(.*)$", lines[i])
        if m:
            fm[m.group(1).strip()] = m.group(2).strip()
    return None, 0


def parse_tables(lines):
    """Kembalikan daftar tabel: dict(heading, start, headers, rows[(lineno, [cells])])."""
    tables, heading, i = [], "", 0
    while i < len(lines):
        ln = lines[i]
        if re.match(r"^#{1,6}\s", ln):
            heading = ln.lstrip("#").strip()
        if ln.strip().startswith("|") and i + 1 < len(lines) and SEP_ROW.match(lines[i + 1]):
            headers = [strip_md(h).lower() for h in split_row(ln)]
            rows, j = [], i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append((j + 1, split_row(lines[j])))
                j += 1
            tables.append({"heading": heading, "start": i + 1, "headers": headers, "rows": rows})
            i = j
            continue
        i += 1
    return tables


def col(headers, *names):
    for idx, h in enumerate(headers):
        for n in names:
            if n in h:
                return idx
    return None


def norm_url(u):
    u = strip_md(u).lower()
    u = re.sub(r"^https?://", "", u)
    u = re.sub(r"^www\.", "", u)
    u = u.rstrip("/")
    m = re.search(r"(10\.\d{4,9}/\S+)", u)
    return m.group(1) if m else u


def has_heading(lines, pattern):
    rx = re.compile(pattern, re.I)
    return any(re.match(r"^#{1,6}\s", ln) and rx.search(ln) for ln in lines)


def word_count(q):
    q = strip_md(q).strip("\"'“”‘’«» ")
    return len(q.split())


def lint(path, hc_csv=None):
    rep = Report()
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    # --- frontmatter
    fm, _ = parse_frontmatter(lines)
    if fm is None:
        rep.add("ERROR", 1, "Frontmatter (--- ... ---) tidak ditemukan.")
        fm = {}
    else:
        idkey = "prompt-id" if "prompt-id" in fm else ("topic" if "topic" in fm else None)
        if idkey is None:
            rep.add("ERROR", 1, "Frontmatter tidak punya `prompt-id` atau `topic`.")
        for key in ("tanggal-jalan", "status", "ringkasan"):
            if key not in fm or not fm[key]:
                rep.add("ERROR", 1, f"Frontmatter tidak punya `{key}`.")
        if not fm.get("model-agent"):
            rep.add("WARN", 1, "Frontmatter tidak punya `model-agent` (boleh `tidak diketahui`).")
        st = fm.get("status", "").strip()
        if st and st not in NOTE_STATUS_OK:
            rep.add("ERROR", 1, f"`status` frontmatter `{st}` tidak dikenal; pilih salah satu {sorted(NOTE_STATUS_OK)}.")
        if st == "diaudit-manusia":
            rep.add("WARN", 1, "`status: diaudit-manusia` hanya boleh ditulis pengguna, bukan agent.")

    # --- bagian wajib
    required = [
        (r"log\s+akses", "Log akses"),
        (r"search\s+log", "Search log"),
        (r"tabel\s+klaim|klaim", "Tabel klaim"),
        (r"keterbatasan", "Keterbatasan"),
        (r"usulan", "Usulan perubahan ke rencana"),
    ]
    for rx, name in required:
        if not has_heading(lines, rx):
            rep.add("ERROR", 1, f"Bagian wajib tidak ada: {name}.")

    tables = parse_tables(lines)

    # --- Log akses
    access = {}  # url_norm -> hasil
    access_text = ""
    scholar_in_access = False
    for t in tables:
        h = t["headers"]
        ci = col(h, "hasil")
        ui = col(h, "url", "doi", "id")
        if ci is None or ui is None or col(h, "alat") is None:
            continue
        for ln, cells in t["rows"]:
            if len(cells) <= max(ci, ui):
                continue
            hasil = strip_md(cells[ci]).lower()
            if hasil not in ACCESS_OK:
                rep.add("ERROR", ln, f"Log akses: `hasil` = `{hasil}` tidak termasuk {sorted(ACCESS_OK)}.")
            access[norm_url(cells[ui])] = hasil
            access_text += " " + cells[ui]
            if "scholar.google" in cells[ui].lower():
                scholar_in_access = True
    if not access and has_heading(lines, r"log\s+akses"):
        rep.add("ERROR", 1, "Log akses ada tetapi tabelnya tidak terbaca atau kosong (kolom: no | URL/DOI/ID | alat | hasil | catatan).")

    # --- Search log
    search_rows = 0
    for t in tables:
        h = t["headers"]
        qi = col(h, "query")
        if qi is None:
            continue
        ji = col(h, "jumlah")
        mi = col(h, "mesin", "situs")
        for ln, cells in t["rows"]:
            search_rows += 1
            if ji is not None and len(cells) > ji:
                v = strip_md(cells[ji]).lower()
                if APPROX.search(cells[ji]):
                    rep.add("ERROR", ln, f"Search log: jumlah hasil `{cells[ji].strip()}` berupa perkiraan; tulis angka persis atau `tidak tersedia`.")
                elif not (re.fullmatch(r"\d+", v) or v == "tidak tersedia"):
                    rep.add("ERROR", ln, f"Search log: jumlah hasil `{cells[ji].strip()}` harus angka atau `tidak tersedia`.")
            if mi is not None and len(cells) > mi and "scholar" in cells[mi].lower() and not scholar_in_access:
                rep.add("WARN", ln, "Search log menyebut Google Scholar, tetapi tidak ada akses ke scholar.google di Log akses.")
    if search_rows == 0 and has_heading(lines, r"search\s+log"):
        rep.add("ERROR", 1, "Search log ada tetapi tidak ada baris query yang terbaca.")

    # --- Tabel klaim
    claim_rows = 0
    neg_status_rows = 0
    for t in tables:
        h = t["headers"]
        si = col(h, "status")
        ki = col(h, "kutipan")
        if si is None or ki is None:
            continue
        ui = col(h, "url")
        vi = col(h, "nilai")
        ci = col(h, "klaim", "pertanyaan")
        for ln, cells in t["rows"]:
            if len(cells) <= max(si, ki):
                continue
            claim_rows += 1
            status = strip_md(cells[si]).upper()
            quote = cells[ki]
            if status not in STATUS_OK:
                rep.add("ERROR", ln, f"Tabel klaim: status `{status}` tidak termasuk {sorted(STATUS_OK)}.")
                continue
            if status == "NOT-FOUND-IN-SEARCH":
                neg_status_rows += 1
            nq = word_count(quote) if strip_md(quote) not in ("", "-", "—", "[VERIFY]") else 0
            if nq > 15:
                rep.add("ERROR", ln, f"Tabel klaim: kutipan {nq} kata (maks 15).")
            if status.startswith("VERIFIED"):
                url = cells[ui] if ui is not None and len(cells) > ui else ""
                if not strip_md(url) or "[VERIFY]" in url:
                    rep.add("ERROR", ln, "Tabel klaim: status VERIFIED-* tetapi URL kosong atau `[VERIFY]`.")
                if nq == 0:
                    rep.add("ERROR", ln, "Tabel klaim: status VERIFIED-* tetapi kutipan kosong.")
                key = norm_url(url) if strip_md(url) else ""
                hit = None
                for ak, av in access.items():
                    if key and (key == ak or key in ak or ak in key):
                        hit = av
                        break
                if key and hit is None:
                    rep.add("ERROR", ln, "Tabel klaim: URL tidak ditemukan di Log akses.")
                elif hit is not None:
                    if status == "VERIFIED-PRIMARY" and hit != "dibuka-penuh":
                        rep.add("ERROR", ln, f"VERIFIED-PRIMARY tetapi di Log akses hasilnya `{hit}` (harus `dibuka-penuh`).")
                    if status == "VERIFIED-SECONDARY" and hit not in ("dibuka-penuh", "hanya-abstrak"):
                        rep.add("ERROR", ln, f"VERIFIED-SECONDARY tetapi di Log akses hasilnya `{hit}`.")
                claim_txt = cells[ci] if ci is not None and len(cells) > ci else ""
                if NEGATIVE_CLAIM.search(claim_txt):
                    rep.add("ERROR", ln, "Klaim berbunyi negatif tetapi berstatus VERIFIED-*; gunakan NOT-FOUND-IN-SEARCH.")
            if status == "NOT-OPENED" and vi is not None and len(cells) > vi:
                v = strip_md(cells[vi])
                if v and v not in ("-", "—", "[VERIFY]", "tidak terbaca"):
                    rep.add("WARN", ln, "NOT-OPENED tetapi kolom nilai terisi; nilai harus dari halaman yang terbuka.")
    if claim_rows == 0 and has_heading(lines, r"tabel\s+klaim|klaim"):
        rep.add("ERROR", 1, "Tabel klaim tidak terbaca (kolom wajib termasuk `kutipan` dan `status`).")
    if neg_status_rows and search_rows == 0:
        rep.add("ERROR", 1, "Ada klaim NOT-FOUND-IN-SEARCH tetapi Search log kosong.")

    # --- seluruh teks
    for n, ln in enumerate(lines, 1):
        if SELF_CERT.search(ln):
            rep.add("ERROR", n, "Kalimat menilai hasil sendiri (lolos/siap lanjut/terverifikasi lengkap); itu wewenang pemeriksa.")
        for d in FORBIDDEN_DOI:
            if d in ln:
                rep.add("ERROR", n, f"DOI terlarang `{d}`.")
    access_blob = access_text.lower()
    seen = set()
    for n, ln in enumerate(lines, 1):
        for m in re.finditer(r"10\.\d{4,9}/[^\s|)\]>`\"']+", ln):
            doi = m.group(0).rstrip(".,;").lower()
            if doi in seen:
                continue
            seen.add(doi)
            if doi not in access_blob and not any(doi in k for k in access):
                rep.add("WARN", n, f"DOI `{doi}` tidak tercatat di Log akses (DOI harus dibaca dari halaman sumber).")

    # --- cek silang CSV HC18
    if hc_csv:
        hc = {}
        with open(hc_csv, newline="", encoding="utf-8-sig") as f:
            r = csv.DictReader(f)
            hc_key = next((k for k in r.fieldnames if "head circumference" in k.lower() or k.lower() in ("hc", "hc_mm")), None)
            fn_key = next((k for k in r.fieldnames if k.lower() in ("filename", "file", "image")), None)
            if not hc_key or not fn_key:
                rep.add("ERROR", 1, f"--hc-csv: kolom filename/HC tidak ditemukan di {hc_csv} ({r.fieldnames}).")
            else:
                for row in r:
                    hc[row[fn_key].replace(".png", "")] = float(row[hc_key])
        if hc:
            for n, ln in enumerate(lines, 1):
                names = set(HC_FILE.findall(ln))
                for nm in names:
                    if nm not in hc:
                        lvl = "ERROR" if re.search(r"_\dHC$", nm) else "WARN"
                        rep.add(lvl, n, f"Nama berkas `{nm}.png` tidak ada di CSV latih ({Path(hc_csv).name}).")
                if len(names) == 1:
                    nm = next(iter(names))
                    m = re.search(r"(?:GT|CSV|HC)\s*[:=]?\s*(\d+(?:[.,]\d+)?)\s*mm", ln)
                    if m and nm in hc:
                        val = float(m.group(1).replace(",", "."))
                        if abs(val - hc[nm]) > 0.05:
                            rep.add("ERROR", n, f"`{nm}.png`: teks menyebut HC {val} mm, CSV resmi {hc[nm]} mm.")
    return rep


def main():
    ap = argparse.ArgumentParser(description="Pemeriksa format Kontrak Output v2 (bukan penilaian isi).")
    ap.add_argument("note", help="berkas catatan .md")
    ap.add_argument("--hc-csv", help="training_set_pixel_size_and_HC.csv untuk mencocokkan nama berkas dan nilai HC yang disebut di teks")
    a = ap.parse_args()
    if not Path(a.note).is_file():
        print(f"Berkas tidak ada: {a.note}", file=sys.stderr)
        sys.exit(2)
    rep = lint(a.note, a.hc_csv)
    print(f"lint_note: {a.note}")
    for lvl, ln, msg in sorted(rep.items, key=lambda x: (x[1], x[0])):
        print(f"[{lvl}] baris {ln}: {msg}")
    e, w = rep.count("ERROR"), rep.count("WARN")
    print(f"Ringkasan: {e} ERROR, {w} WARN. Pemeriksaan format dan konsistensi internal saja; bukan penilaian kebenaran isi.")
    sys.exit(1 if e else 0)


if __name__ == "__main__":
    main()
