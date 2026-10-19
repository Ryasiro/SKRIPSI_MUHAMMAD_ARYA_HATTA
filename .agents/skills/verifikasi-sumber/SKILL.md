---
name: verifikasi-sumber
description: Verifikasi independen atas satu catatan riset, dikerjakan di percakapan baru. Membuka ulang SETIAP sumber di tabel klaim dan membandingkan dengan kutipan yang dicatat. Jalankan hanya jika pengguna mengetik /verifikasi-sumber diikuti jalur berkas catatan.
---

# Verifikasi sumber (percakapan baru, tanpa konteks penulis)

Jalankan skill ini di percakapan yang **belum pernah** dipakai menulis catatan tersebut. Kamu hanya punya berkas catatan dan akses ke sumber. Ikuti Kontrak Output v2 di `AGENTS.md`.

Masukan: jalur berkas catatan, misalnya `research-notes/<slug>.md`. Keluaran: `research-notes/<slug>.verifikasi.md`. Jangan mengedit berkas catatan aslinya.

## Langkah

1. Baca catatan. Daftar semua baris di Tabel klaim, **seluruhnya, bukan sampel**. Jika jumlahnya lebih dari 40, kerjakan 40 pertama berdasarkan ID, lalu tulis di Keterbatasan bagian mana yang belum diperiksa.
2. Untuk setiap baris, buka sendiri URL-nya dan cari nilai yang diklaim di lokasi bukti yang ditulis. Catat pembukaan itu di Log akses milikmu (bukan menyalin log penulis).
3. Isi tabel verifikasi: `ID | dibuka ulang? | nilai menurut verifikator | kutipan verifikator (maks 15 kata) | hasil | catatan`.
   Nilai `hasil`:
   - `COCOK`: nilai dan makna sama dengan klaim.
   - `BEDA-ANGKA`: angka, tahun, nama, atau halaman berbeda. Tulis kedua nilai.
   - `BEDA-MAKNA`: angkanya ada tetapi sumber mengatakan hal yang berbeda atau lebih sempit (mis. nilai itu milik subset data, bukan seluruh data).
   - `TIDAK-ADA-DI-SUMBER`: halaman terbuka, tetapi klaim tidak ditemukan di lokasi yang disebut atau di tempat lain pada halaman itu.
   - `TIDAK-TERBUKA`: halaman gagal dibuka atau tabel/gambar tidak terbaca.
4. Untuk klaim negatif (`NOT-FOUND-IN-SEARCH`), jalankan ulang minimal dua query berbeda dari yang dicatat penulis dan laporkan apa yang muncul. Jangan menyatakan klaim negatif benar atau salah; laporkan temuan pencarianmu.
5. Periksa metadata sitasi tiap sumber (penulis, tahun, venue, volume, halaman, DOI) langsung dari halaman sumber dan catat selisihnya.
6. Tutup dengan ringkasan hitungan: jumlah baris per nilai `hasil`. Jangan menulis "lolos" atau "tidak lolos". Jangan mengubah `status` di catatan asli. Jalankan `python scripts/lint_note.py research-notes/<slug>.verifikasi.md` dan tempel hasilnya.

## Setelah selesai
Pengguna yang memutuskan. Skill ini hanya menyediakan hitungan dan selisih. Jika seluruh tabel selesai dikerjakan (bukan terpotong di langkah 1), pengguna dapat mengganti `status` catatan menjadi `diverifikasi-agent`. Nilai `diaudit-manusia` hanya untuk pengguna.
