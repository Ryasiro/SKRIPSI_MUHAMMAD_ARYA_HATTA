---
name: riset-literatur
description: Riset literatur terstruktur untuk satu pertanyaan riset skripsi (rencana, pencarian, pembukaan sumber, tabel klaim, sintesis bersyarat). Jalankan hanya jika pengguna mengetik /riset-literatur atau meminta riset literatur secara eksplisit. Bukan untuk mencari satu fakta cepat.
---

# Riset literatur terstruktur

Skill ini menggantikan pipeline lama (planner, researcher, verifier, synthesizer, citation-manager) yang berjalan beruntun di satu percakapan. Di sini tahap 1 sampai 5 dikerjakan di satu percakapan, tetapi **verifikasi dilakukan di percakapan baru** lewat skill `verifikasi-sumber`, supaya pemeriksa tidak membawa asumsi penulisnya. Ikuti Kontrak Output v2 di `AGENTS.md`.

Masukan dari pengguna: pertanyaan riset dan (opsional) slug nama berkas. Jika slug tidak diberikan, buat huruf kecil dengan tanda hubung, maksimal lima kata. Keluaran: `research-notes/<slug>.md`.

## Langkah

0. **Lanjutkan atau mulai.** Jika `research-notes/<slug>.md` sudah ada, ikuti bagian "Melanjutkan" di skill `catatan-riset`. Jangan menimpa.

1. **Rencana.** Pecah pertanyaan menjadi 3 sampai 7 sub-pertanyaan. Tiap sub-pertanyaan berisi: tag singkat, jenis (`fakta`, `perbandingan`, atau `klaim-negatif`), dan **satu query penyangkal**, yaitu pencarian yang sengaja mencari bukti bahwa dugaan awal salah. Tulis dugaan awal sebagai dugaan yang akan diuji, bukan sebagai jawaban.

2. **Pencarian.** Jalankan pencarian per sub-pertanyaan dan catat setiap query di Search log. Prioritaskan halaman penerbit, PubMed Central, arXiv, Semantic Scholar, DBLP, dan repositori resmi. Google Scholar dicatat hanya jika benar-benar bisa diakses oleh alatmu; jika tidak, jangan disebut.

3. **Buka sumbernya.** Setiap sumber yang akan dikutip harus dibuka, bukan dikenali dari judul. Catat di Log akses. Jika hanya abstrak yang terbaca, statusnya maksimal `VERIFIED-SECONDARY`. Jika gagal dibuka, `NOT-OPENED`.

4. **Ekstraksi klaim.** Isi Tabel klaim: satu baris per klaim, dengan nilai, lokasi bukti, dan kutipan maksimal 15 kata. Metadata sitasi (penulis, tahun, venue, volume, halaman, DOI) diambil dari halaman yang dibuka dan dicatat sebagai klaim juga; yang tidak terbaca ditulis `[VERIFY]`.

5. **Sintesis bersyarat.** Tulis narasi hanya dari klaim berstatus `VERIFIED-*`. Setiap kalimat narasi diberi ID klaim, misalnya `[C3]`. Klaim `NOT-OPENED` dikumpulkan di bagian "Belum bisa dipakai". Bagian "Celah" ditulis dengan bahasa "dalam pencarian ini belum ditemukan" dan merujuk ke baris Search log yang mendukungnya.

6. **Simpan dan berhenti.** Simpan dengan `status: draft`. Jalankan `python scripts/lint_note.py research-notes/<slug>.md` dan tempel hasilnya di bagian akhir. Beri tahu pengguna bahwa langkah berikutnya adalah membuka percakapan baru dan menjalankan `/verifikasi-sumber research-notes/<slug>.md`. Jangan menilai sendiri bahwa hasilnya cukup.

## Yang tidak boleh
- Menulis daftar pustaka dari ingatan. Daftar pustaka dibuat dari klaim metadata yang berstatus `VERIFIED-*` memakai skill `format-sitasi`.
- Menghapus atau mengganti baris Search log atau Log akses setelah ditulis. Koreksi ditambahkan sebagai baris baru.
- Menyebut "semua sumber terverifikasi". Verifikasi adalah pekerjaan skill lain di percakapan lain.
