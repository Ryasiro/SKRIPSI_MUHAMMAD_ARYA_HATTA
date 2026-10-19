#!/usr/bin/env python3
"""rapikan_repo.py - merapikan repositori skripsi lama menjadi workspace baru.

Apa yang dilakukan (urutan):
  1. Memeriksa bahwa folder ini repositori git dan working tree-nya bersih.
  2. Mencadangkan data/hc18 ke folder cadangan DI LUAR repositori (diverifikasi jumlah berkasnya).
  3. Berhenti-melacak (git rm --cached) data/hc18 dan data/hc18_derived. Berkasnya tetap ada di disk.
  4. Memindahkan hasil lama (.claude/, research-notes/, splits/, scripts/, data/hc18_derived/,
     ringkasan lama, README lama) ke folder arsip DI LUAR repositori, supaya agent baru tidak membacanya.
  5. Membuat ulang kerangka folder kosong dan menambahkan aturan ke .gitignore.
  6. Menyalin isi workspace baru (folder tempat skrip ini berada, tanpa .gitignore dan .git) ke repositori.

Tidak melakukan commit dan tidak pernah melakukan push. Default-nya DRY-RUN (hanya mencetak rencana);
tambahkan --apply untuk benar-benar menjalankan. Jika sedang di branch main/master, --apply membuat
branch baru `rapikan-workspace` terlebih dahulu.

Pemakaian: ekstrak zip workspace ke folder TERPISAH (di luar repositori), lalu dari situ jalankan:
    python tools/rapikan_repo.py --repo <jalur repositori lama> --arsip <folder arsip> --backup <folder cadangan>
    python tools/rapikan_repo.py --repo <jalur repositori lama> --arsip <folder arsip> --backup <folder cadangan> --apply
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

DATA_TRACKED = ["data/hc18", "data/hc18_derived"]
TO_ARCHIVE = [
    ".claude",
    "research-notes",
    "splits",
    "scripts",
    "data/hc18_derived",
    "skripsi-usg-kepala-janin-summary.md",
    "README.md",
]
SKELETON = ["research-notes", "splits", "scripts", "data", "docs", "tools"]
IGNORE_LINES = [
    "# --- data dan keluaran besar (jangan di-commit) ---",
    "data/hc18/",
    "data/hc18_derived*/",
    "*.pt",
    "*.onnx",
    "runs/",
    "weights/",
    "*.zip",
    "# --- python / notebook ---",
    "__pycache__/",
    "*.py[cod]",
    ".venv/",
    "venv/",
    ".ipynb_checkpoints/",
    "# --- lain-lain ---",
    ".DS_Store",
    "Thumbs.db",
]


def git(repo, *args, check=True):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        sys.exit(f"git {' '.join(args)} gagal:\n{r.stderr.strip()}")
    return r.stdout.strip()


def count_files(p):
    return sum(1 for x in Path(p).rglob("*") if x.is_file())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", required=True, help="root repositori lama yang akan dirapikan")
    ap.add_argument("--arsip", required=True, help="folder arsip DI LUAR repositori")
    ap.add_argument("--backup", required=True, help="folder cadangan data/hc18 DI LUAR repositori")
    ap.add_argument("--apply", action="store_true", help="jalankan sungguhan (tanpa ini hanya dry-run)")
    a = ap.parse_args()

    repo = Path(a.repo).resolve()
    arsip = Path(a.arsip).resolve()
    backup = Path(a.backup).resolve()
    if not (repo / ".git").exists():
        sys.exit(f"{repo} bukan root repositori git.")
    for name, p in (("arsip", arsip), ("backup", backup)):
        if repo == p or repo in p.parents:
            sys.exit(f"Folder {name} ({p}) harus berada DI LUAR repositori.")
    if git(repo, "status", "--porcelain"):
        sys.exit("Working tree belum bersih. Commit atau stash perubahanmu dulu, lalu jalankan lagi.")

    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    mode = "SUNGGUHAN" if a.apply else "DRY-RUN"
    print(f"[{mode}] repo={repo}\n  branch saat ini: {branch}\n  arsip : {arsip}\n  backup: {backup}")

    src_data = repo / "data" / "hc18"
    if not src_data.is_dir():
        print("  ! data/hc18 tidak ditemukan; langkah cadangan dilewati.")
    plan = []
    if src_data.is_dir():
        plan.append(f"salin data/hc18 ({count_files(src_data)} berkas) -> {backup}/hc18")
    plan.append("git rm -r --cached " + " ".join(p for p in DATA_TRACKED if (repo / p).exists()))
    for item in TO_ARCHIVE:
        if (repo / item).exists():
            plan.append(f"pindahkan {item} -> {arsip}/{item}")
    plan.append("buat ulang kerangka: " + ", ".join(SKELETON))
    plan.append("tambahkan aturan ke .gitignore (idempoten)")
    ws = Path(__file__).resolve().parent.parent
    if ws == repo:
        sys.exit("Skrip ini harus dijalankan dari salinan workspace yang TERPISAH dari repositori (lihat petunjuk di atas).")
    plan.append(f"salin isi workspace baru dari {ws} ke repositori")
    print("\nRencana:")
    for i, p in enumerate(plan, 1):
        print(f"  {i}. {p}")
    if branch in ("main", "master") and a.apply:
        print("  (branch main/master terdeteksi: akan membuat branch `rapikan-workspace`)")
    if not a.apply:
        print("\nDry-run selesai. Tidak ada yang diubah. Tambahkan --apply untuk menjalankan.")
        return

    if branch in ("main", "master"):
        git(repo, "checkout", "-b", "rapikan-workspace")
        print("Branch baru: rapikan-workspace")

    # 2. cadangan
    if src_data.is_dir():
        dst = backup / "hc18"
        if dst.exists():
            sys.exit(f"{dst} sudah ada. Pindahkan atau pilih folder cadangan lain.")
        backup.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src_data, dst)
        n_src, n_dst = count_files(src_data), count_files(dst)
        if n_src != n_dst:
            sys.exit(f"Cadangan tidak lengkap ({n_dst}/{n_src} berkas). Dihentikan sebelum ada perubahan lain.")
        print(f"Cadangan OK: {n_dst} berkas di {dst}")

    # 3. berhenti melacak data
    for p in DATA_TRACKED:
        if (repo / p).exists():
            git(repo, "rm", "-r", "--cached", "-q", p)
    print("Data tidak lagi dilacak git (berkas di disk tetap ada).")

    # 4. arsip
    arsip.mkdir(parents=True, exist_ok=True)
    for item in TO_ARCHIVE:
        s = repo / item
        if not s.exists():
            continue
        d = arsip / item
        d.parent.mkdir(parents=True, exist_ok=True)
        if d.exists():
            sys.exit(f"{d} sudah ada di arsip; dihentikan.")
        shutil.move(str(s), str(d))
        print(f"Dipindah: {item} -> {d}")

    # 5. kerangka dan .gitignore
    for d in SKELETON:
        (repo / d).mkdir(parents=True, exist_ok=True)
    for d in ("research-notes", "splits", "scripts"):
        (repo / d / ".gitkeep").touch()
    gi = repo / ".gitignore"
    existing = gi.read_text(encoding="utf-8").splitlines() if gi.exists() else []
    add = [ln for ln in IGNORE_LINES if ln not in existing]
    if add:
        with open(gi, "a", encoding="utf-8") as f:
            if existing and existing[-1].strip():
                f.write("\n")
            f.write("\n".join(add) + "\n")

    # 6. salin workspace baru
    def _skip(d, names):
        return [n for n in names if n in (".git", "__pycache__") or (Path(d) == ws and n == ".gitignore")]
    shutil.copytree(ws, repo, dirs_exist_ok=True, ignore=_skip)
    print(f"Workspace baru disalin dari {ws}")

    print("\nSelesai. Berikutnya (kamu yang menjalankan):")
    print("  1. Buka repositori ini dan periksa hasilnya.")
    print("  2. git status    # pastikan data/hc18 TIDAK muncul sebagai file baru")
    print("  3. git add -A && git commit -m \"Rapikan workspace: skill Antigravity, data tidak dilacak\"")
    print("  4. JANGAN checkout ke commit lama lalu kembali tanpa cadangan: berpindah dari commit yang")
    print("     melacak data ke commit yang tidak melacaknya akan menghapus berkas data dari folder kerja.")
    print(f"     Cadangan ada di: {backup}")
    print("  5. Push hanya ke branch ini (bukan main), dan hanya jika kamu sudah memeriksa hasilnya.")


if __name__ == "__main__":
    main()
