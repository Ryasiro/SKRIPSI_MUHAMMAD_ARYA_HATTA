---
name: hc18-p4-data
description: Inspeksi dataset HC18 lokal, grouping per prefiks nama file, group 5-fold terstratifikasi seed 42, hitung ulang HC dari anotasi, dan floor per pipeline, dengan skrip verifikasi independen. Jalankan hanya jika pengguna mengetik /hc18-p4-data atau meminta P4 HC18 secara eksplisit.
---

# P4. Inspeksi data HC18

Ikuti Kontrak Output v2 dan aturan pekerjaan kode di `AGENTS.md`. Laporan: `research-notes/hc18-P4-inspeksi-data.md`. Log mentah: `research-notes/hc18-P4-log/`.

Data ada di `data/hc18/` (baca-saja). Jika belum ada, berhenti dan beri tahu pengguna agar mengunduh dari Zenodo (DOI 10.5281/zenodo.1322001). Jangan mengunduh dari sumber lain.

Jangan membuka atau membandingkan dengan hasil lama jika ada di workspace (mis. `splits/hc18_group5fold_seed42.csv`, `data/hc18_derived/`). Semua yang kamu hasilkan memakai akhiran `_ag` agar tidak menimpa apa pun.

## Langkah (jalankan kode sungguhan, simpan stdout ke log)
1. **Struktur berkas** apa adanya: jumlah citra dan anotasi latih, jumlah citra uji, nama dan kolom CSV.
2. **Group** dari angka di awal nama file (regex `^\d+_`): jumlah group, distribusi ukuran group, jumlah group dengan lebih dari satu citra beserta jumlah citranya.
3. **CSV:** nilai kosong; rentang ukuran piksel dan rentang HC untuk latih dan uji; nama berkas yang menjadi min dan maks ukuran piksel.
4. **Konsistensi dalam group:** proporsi group multi-citra dengan ukuran piksel identik; sebaran CV HC dalam group (std/mean) dibanding CV seluruh data; daftar group dengan CV HC > 0,08. Tulis interpretasi sebagai hipotesis, bukan bukti pasti.
5. **Hitung ulang HC dari anotasi**, dua cara, dilaporkan terpisah dan diberi nama jujur:
   - (a) fit elips (`cv2.fitEllipse`) langsung pada piksel garis anotasi, rumus Ramanujan, kali ukuran piksel. Laporkan MAE, median, p95, maks terhadap HC di CSV dengan label "kesesuaian CSV dengan fit kontur". Jangan menyebutnya error floor.
   - (b) pipeline mask: isi elips hasil fit menjadi mask biner, ambil kontur terbesar, fit elips lagi, Ramanujan. Laporkan MAE, median, p95, maks; juga per kuartil ukuran piksel; 10 kasus terburuk dengan nama berkas dan ukuran piksel.
   - (c) seperti (b) setelah mask di-resize ke skala 0,64; 0,48; dan 0,32, dalam dua mode: nearest (mask keras di resolusi rendah) dan soft (area-resize, upsample bilinear, ambang 0,5).
   - Laporkan jumlah anotasi yang menyentuh tepi citra, bagaimana mask diisi untuk kasus itu, dan apakah kasus terburuk termasuk di dalamnya.
6. **Floor untuk deteksi OBB:** dari parameter elips, bentuk empat sudut oriented box, normalisasi koordinat dengan lebar dan tinggi citra, bulatkan enam desimal (format label YOLO OBB), pulihkan elips dari empat titik itu (`cv2.minAreaRect`), hitung HC, laporkan selisih terhadap HC dari fit awal dan terhadap HC di CSV.
7. **Group 5-fold:** `StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)`, label stratifikasi lima bin kuantil HC (`pd.qcut`), group dari langkah 2. Simpan `splits/hc18_group5fold_seed42_ag.csv` dengan kolom `filename, group, fold, hc_mm, pixel_size_mm, hc_bin` dan skrip `scripts/make_folds_ag.py`. Jika berkas dengan nama itu sudah ada, berhenti dan laporkan. Verifikasi leakage dengan menghitung ulang group dari kolom `filename` di berkas split (bukan dari kolom `group`) dan pastikan setiap group hanya di satu fold. Ringkas ukuran, jumlah group, dan statistik HC per fold. Tulis juga `splits/hc18_group5fold_seed42_ag.meta.json` berisi versi `python`, `numpy`, `pandas`, `scikit-learn`, `opencv` dan checksum SHA-256 berkas split. Jalankan pembuatan fold dua kali dan laporkan apakah hasilnya identik di mesin yang sama.
8. **Turunan:** mask terisi ke `data/hc18_derived_ag/masks/`; `data/hc18_derived_ag/ellipse_parameters.csv` (pusat, sumbu penuh dalam piksel, sudut, empat sudut OBB ternormalisasi); 12 overlay sampel acak (seed 42) ke `research-notes/hc18-P4-overlays-ag/`. Skrip yang sama menulis `research-notes/hc18-P4-overlays-ag/overlay_index.csv` (nama berkas, HC di CSV, HC dari elips fit, selisih). Tabel overlay di laporan disalin dari berkas itu, tidak ditulis tangan.
9. **Verifikasi independen:** `scripts/verify_hc18.py` sudah disediakan pengguna; jangan mengubahnya. Jalankan:
   `python scripts/verify_hc18.py --data data/hc18 --splits splits/hc18_group5fold_seed42_ag.csv | tee research-notes/hc18-P4-log/verify_hc18.txt`
   Tempel keluaran mentahnya di laporan. Bandingkan dengan langkah 1 sampai 8. Setiap ketidakcocokan dilaporkan dan dijelaskan, tidak dihaluskan.

## Laporan
Berisi perintah persis yang dijalankan, keluaran ringkas, tabel hasil, daftar berkas yang dibuat, dan bagian Keterbatasan. Di Keterbatasan tulis bahwa hubungan antara prefiks nama file dan pasien tidak bisa diketahui dari data publik, sehingga group mewakili pemeriksaan menurut prefiks. Jangan menyebut group sebagai pasien atau janin.
