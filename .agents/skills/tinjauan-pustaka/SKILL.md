---
name: tinjauan-pustaka
description: Struktur bagian tinjauan pustaka (landasan teori, penelitian terkait dengan tabel pembanding, celah penelitian) dari catatan riset yang sudah diverifikasi. Jalankan hanya jika pengguna mengetik /tinjauan-pustaka atau meminta draf tinjauan pustaka secara eksplisit.
---

# Tinjauan pustaka

Skill ini menyusun teks dari catatan riset. Ia tidak mencari sumber baru. Masukan: satu atau lebih berkas `research-notes/*.md` yang pengguna tunjuk. Pakai hanya klaim `VERIFIED-*`. Jika catatan masih `draft` dan belum punya berkas `.verifikasi.md`, tulis peringatan itu di awal keluaran.

## Struktur
1. **Landasan teori:** konsep dan definisi yang dibutuhkan pembaca. Kutip sumber kanonik atau primer tiap konsep.
2. **Penelitian terkait:** urut kronologis atau tematis, tidak dicampur. Sertakan tabel:

   | No | Penulis (Tahun) | Dataset dan protokol split | Metode | Hasil (angka dari sumber) | Perbedaan spesifik dengan penelitian ini | Klaim terkait |
   |----|-----------------|----------------------------|--------|---------------------------|------------------------------------------|---------------|

   - `Dataset dan protokol split` memuat tingkat pemisahan (citra, pemeriksaan, pasien) dan set evaluasinya. Jika makalah tidak menyebut, tulis `tidak dilaporkan`.
   - `Hasil` hanya berisi angka yang ada di klaim `VERIFIED-*`, dengan satuan dan definisi metrik.
   - `Perbedaan spesifik` menyebut dataset, protokol, metode, atau skala yang berbeda. Jangan menulis kalimat umum seperti "belum ada yang meneliti ini".
   - `Klaim terkait` memuat ID klaim pendukung, mis. `C3, C7`.
3. **Kerangka berpikir dan celah:** pernyataan celah ditulis dari bagian "Celah" di catatan riset dengan bahasa "dalam pencarian ini belum ditemukan", dan merujuk ke query di Search log. Perbandingan antar-angka dari makalah dengan protokol berbeda diberi catatan bahwa angkanya tidak sebanding langsung.

## Mutu minimum
- Setiap kalimat klaim punya sitasi dan ID klaim. Kalimat tanpa sumber ditandai `[NEEDS SOURCE]`.
- Daftar pustaka dibuat dengan skill `format-sitasi` sebagai blok terpisah di akhir.
- Keluaran adalah draf Markdown. Pengguna dan dosen pembimbing yang memutuskan isi akhir.
