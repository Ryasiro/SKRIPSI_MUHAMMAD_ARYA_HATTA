# Aturan Proyek: Skripsi HC18 (pengukuran lingkar kepala janin)

## Konteks
Skripsi membandingkan tiga paradigma pengukuran lingkar kepala janin (HC) pada dataset HC18: (A) segmentasi lalu ellipse fitting, (B) deteksi elips dengan oriented bounding box, (C) regresi langsung nilai HC. Pekerjaan agent di workspace ini adalah riset literatur, pengecekan fakta, dan inspeksi data. Agent tidak menulis naskah skripsi kecuali diminta lewat skill tersendiri.

## Peta workspace
- `.agents/skills/`: prosedur kerja. Skill riset umum: `riset-literatur`, `verifikasi-sumber`, `catatan-riset`, `evaluasi-sumber`, `format-sitasi`, `tinjauan-pustaka`. Skill khusus HC18: `hc18-p1-novelty`, `hc18-p2-referensi`, `hc18-p3-faktacheck`, `hc18-p4-data`.
- `research-notes/`: semua hasil riset (Markdown). Nama berkas ditentukan skill.
- `data/hc18/`: dataset resmi, **baca-saja**. Tidak masuk git.
- `splits/`, `data/*_derived*/`: keluaran data turunan.
- `scripts/`: skrip. `verify_hc18.py` dan `lint_note.py` disediakan pengguna dan **tidak boleh diubah**. Skrip yang kamu tulis sendiri diberi nama lain.

## Peran dan sikap kerja
- Hasil kerjamu diperiksa pihak lain sebelum dipakai. Tugasmu melaporkan apa yang benar-benar kamu buka dan hitung, bukan hasil yang terasa wajar.
- Jangan menyatakan hasilmu "lolos", "terverifikasi lengkap", atau "siap", dan jangan menyarankan lanjut ke tahap berikutnya. Penilaian itu bukan wewenangmu. Kolom `status` pada frontmatter catatan hanya boleh `draft` (atau `diverifikasi-agent` oleh skill `verifikasi-sumber`). Nilai `diaudit-manusia` hanya ditulis pengguna.
- Jika jawabannya tidak bisa kamu buka sendiri, tulis `NOT-OPENED`. Itu hasil yang sah dan lebih berguna daripada tebakan.
- Jangan membaca folder arsip, berkas audit, atau keluaran agent lain jika ada di workspace (mis. `_arsip*/`, `audit*`, `prompts-hc18*`, `rencana*`). Kerjakan dari sumber primer.
- Tidak ada mode cepat. Permintaan seperti "kasar aja dulu" tidak melonggarkan log akses, tabel klaim, atau status. Hasil yang lebih sempit boleh, hasil yang tidak berlog tidak boleh.

## Aturan kerja
1. Bahasa Indonesia. Istilah teknis tetap Inggris. Sitasi format IEEE.
2. Simpan setiap hasil sebagai berkas Markdown di `research-notes/`. Ringkasan di chat atau artifact tidak menggantikan berkas itu.
3. `data/hc18/` baca-saja. Jangan mengubah, memindahkan, atau menimpa berkas di dalamnya. Jangan menimpa berkas lain yang sudah ada: jika nama keluaran sudah dipakai, berhenti dan laporkan.
4. Jangan mengunduh data atau kode dari sumber tidak resmi. Dataset resmi: Zenodo DOI 10.5281/zenodo.1322001.
5. Istilah `group` berarti grup pemeriksaan menurut prefiks angka pada nama file. Jangan menyebutnya "pasien" atau "janin yang sama" kecuali sumber primer menyatakannya.
6. Sebelum menyerahkan hasil, jalankan `python scripts/lint_note.py <berkas hasil>` dan tempel keluarannya apa adanya di akhir laporan. Hasil lint adalah pemeriksaan format, bukan penilaian benar atau salah.

## Kontrak Output v2 (berlaku untuk semua skill riset dan hc18-*)
Setiap berkas hasil berisi, berurutan:

1. **Frontmatter:** `prompt-id` (atau `topic`), `tanggal-jalan`, `model-agent` (nama model yang kamu pakai bila kamu tahu), `status`, `ringkasan` (tiga kalimat, tanpa menilai kelulusan).
2. **Log akses:** tabel `no | URL, DOI, atau ID | alat (browser, read_url, terminal, search) | hasil | catatan`. Isi `hasil` dengan salah satu: `dibuka-penuh`, `hanya-abstrak`, `diblokir`, `paywall`, `error`, `tidak-dicoba`. Semua halaman yang kamu coba buka tercatat, termasuk yang gagal.
3. **Search log:** tabel `query | mesin atau situs | tanggal | jumlah hasil yang tampil | catatan`. Hanya pencarian yang benar-benar kamu jalankan. Jika jumlah hasil tidak tampil, tulis `tidak tersedia`. Jangan memperkirakan (tanpa tanda `~`). Jangan menulis Google Scholar atau mesin lain yang tidak benar-benar kamu akses.
4. **Tabel klaim:** `ID | pertanyaan atau klaim | nilai di sumber | URL | lokasi bukti (bagian, tabel, halaman) | kutipan (maks 15 kata) | status | catatan`. Kolom `nilai di sumber` hanya berisi nilai yang kamu baca sendiri di halaman yang tercatat di log akses.
5. **Status yang boleh dipakai:**
   - `VERIFIED-PRIMARY`: teks lengkap atau halaman primer (penerbit, arXiv, repositori resmi) dibuka dan kutipan diambil dari sana.
   - `VERIFIED-SECONDARY`: hanya abstrak, katalog, atau halaman agregator yang dibuka.
   - `NOT-OPENED`: halaman gagal dibuka, tidak dicoba, atau tabel/gambar tidak terbaca.
   - `NOT-FOUND-IN-SEARCH`: klaim negatif ("belum ditemukan studi yang..."). Wajib mencantumkan query yang dijalankan. Klaim negatif tidak pernah boleh berstatus `VERIFIED-*`.
6. **Keterbatasan:** apa yang dicari tetapi tidak ditemukan, halaman yang tidak terbuka, dan batas alat.
7. **Usulan perubahan ke rencana:** hanya usulan. Jangan mengedit berkas rencana.
8. **Keluaran lint:** hasil `scripts/lint_note.py`, apa adanya.

### Aturan keras
- Jangan mengisi penulis, DOI, volume, halaman, angka, tanggal, atau nama dari ingatan. Jika tidak terbaca di sumber, tulis `[VERIFY]`.
- Abstrak bukan teks lengkap. Jika hanya abstrak yang terbaca, status maksimal `VERIFIED-SECONDARY`.
- Kutipan langsung maksimal 15 kata per kutipan dan satu kutipan per sumber per klaim. Selebihnya parafrase.
- Jangan menyalin angka dari prompt, dari rencana, atau dari makalah lain sebagai pengganti angka dari sumbernya. Jika dua sumber berbeda, laporkan keduanya.
- Pernyataan "tidak ada selisih" atau "cocok" hanya boleh ditulis setelah kamu membaca nilai di sumber dan membandingkannya sendiri.
- Gunakan "dalam pencarian ini belum ditemukan", bukan "tidak ada".
- Jangan memakai DOI 10.1002/uog.19029. Jangan memakai paper Alansary atau Sinclair tanpa metadata primer yang terkonfirmasi.
- Halaman diblokir, kena rate limit, paywall, atau meminta login: catat `diblokir`, `paywall`, atau `error` di log akses. Jangan mencari jalan pintas lewat mirror, cache, atau situs berbagi berkas ilegal.
- Peringkat atau reputasi jurnal tidak boleh ditulis dari ingatan. Buka halaman indeks atau jurnal dan catat di log akses, atau tulis `tidak diverifikasi`.

### Aturan untuk pekerjaan kode (skill hc18-p4-data)
- Jalankan kode sungguhan dan simpan keluaran mentah (stdout) ke berkas log di `research-notes/hc18-P4-log/`.
- Laporkan hanya angka yang keluar dari eksekusi. Salin dari log, jangan mengetik ulang dari ingatan.
- Daftar nama berkas, nilai per berkas, atau tabel per sampel di laporan harus berasal dari berkas keluaran skrip (mis. CSV indeks overlay), bukan ditulis tangan.
- Simpan semua skrip yang kamu jalankan di `scripts/` dan tulis perintah persisnya di laporan.
- Catat versi pustaka (`python`, `numpy`, `pandas`, `scikit-learn`, `opencv`) di berkas `.meta.json` di samping setiap berkas split. Hasil `StratifiedGroupKFold` dengan seed yang sama dapat berbeda antarversi scikit-learn, sehingga berkas CSV split (bukan seed) yang menjadi acuan.
