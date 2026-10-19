# Skripsi HC18: fungsi loss berbasis kontur pada U-Net untuk segmentasi dan pengukuran lingkar kepala janin (HC)

**Judul:** Pengaruh Fungsi Loss Berbasis Kontur pada U-Net terhadap Akurasi Segmentasi dan Pengukuran Lingkar Kepala Janin pada Citra USG HC18 dengan Validasi Berbasis Subjek

Workspace untuk riset literatur, pengecekan fakta, dan inspeksi data skripsi, dirancang untuk Antigravity (juga terbaca oleh agent lain yang mengikuti `AGENTS.md`).

Riwayat judul: pada 2026-10-19 judul diganti dari rancangan perbandingan tiga paradigma pengukuran HC. Ringkasan konteks baru ada di bagian Konteks `AGENTS.md`.

## Isi
```
AGENTS.md                  aturan proyek + Kontrak Output v2 (dibaca otomatis oleh agent)
CLAUDE.md                  satu baris, menunjuk ke AGENTS.md (kompatibilitas)
.agents/skills/            prosedur kerja, satu folder per skill
  riset-literatur          riset terstruktur untuk satu pertanyaan  (/riset-literatur)
  verifikasi-sumber        verifikasi independen, di percakapan BARU (/verifikasi-sumber)
  catatan-riset            format catatan dan cara melanjutkan
  evaluasi-sumber          kriteria menilai sumber, termasuk pencitraan medis
  format-sitasi            IEEE (bawaan) dan APA
  tinjauan-pustaka         susunan Bab 2 dari catatan terverifikasi
  hc18-p1-novelty ... hc18-p4-data   tugas khusus HC18 (celah loss berbasis kontur, referensi, fact-check, inspeksi data)
scripts/
  lint_note.py             memeriksa format hasil agent; --hc-csv mencocokkan nama berkas dan nilai HC
  verify_hc18.py           pengecekan independen data HC18 (hanya membaca)
tools/rapikan_repo.py      sekali pakai: merapikan repositori lama
data/hc18/                 dataset resmi (tidak di-commit; lihat data/README.md)
research-notes/            semua hasil riset
splits/                    berkas fold
```

## Alur kerja
1. Jalankan satu skill per percakapan baru. Hasilnya berkas di `research-notes/`.
2. Jalankan `python scripts/lint_note.py research-notes/<berkas>.md` (agent sudah diminta menjalankannya, tetapi jalankan juga sendiri).
3. Untuk riset umum: `/verifikasi-sumber research-notes/<slug>.md` di percakapan baru.
4. Hasil yang akan dipakai di naskah diperiksa manusia (kamu, dosen pembimbing) atau diaudit di luar workspace. Nilai `status: diaudit-manusia` hanya kamu yang menulis.

## Pengaturan Antigravity yang disarankan
- Permission `Default` atau `Request Review`, bukan `Turbo`.
- Model berbeda untuk verifikasi daripada untuk penulisan, supaya kesalahan tidak ikut terbawa.
- Setujui akses web satu per satu; baca perintah terminal sebelum menyetujui yang di luar sandbox.

## Aturan menjaga independensi
- Jangan menaruh berkas audit, kunci jawaban, atau hasil agent lain di folder ini. Simpan di folder terpisah di luar workspace (mis. `../skripsi-arsip/`).
- Berkas split (`splits/*.csv`) yang menjadi acuan dibekukan dengan checksum SHA-256 setelah dipilih. Seed saja tidak cukup: hasil `StratifiedGroupKFold` bergantung pada versi scikit-learn.
- Jangan commit data mentah, bobot model, atau berkas besar (`.gitignore` sudah mengatur).
