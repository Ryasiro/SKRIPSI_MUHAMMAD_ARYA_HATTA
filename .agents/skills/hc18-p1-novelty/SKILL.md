---
name: hc18-p1-novelty
description: Menguji tiga hipotesis research gap HC18 (perbandingan tiga paradigma, risiko split tanpa grouping, YOLO26 dan backbone regresi modern) lewat pencarian literatur dan tabel split per makalah. Jalankan hanya jika pengguna mengetik /hc18-p1-novelty atau meminta P1 HC18 secara eksplisit.
---

# P1. Uji novelty tiga hipotesis gap

Ikuti Kontrak Output v2 di `AGENTS.md`. Keluaran: `research-notes/hc18-P1-novelty.md`.

## Hipotesis (tugasmu mencoba membantahnya, bukan mengonfirmasinya)
- **G1.** Tidak ada makalah yang membandingkan tiga paradigma dalam satu protokol yang sama pada HC18: (A) segmentasi lalu ellipse fitting, (B) deteksi elips berorientasi (oriented box), (C) regresi langsung nilai HC.
- **G2.** Set uji HC18 tidak berlabel publik, sehingga banyak studi membagi ulang 999 citra latih. Sebagian mungkin membagi tanpa grouping per pemeriksaan. Seberapa sering hal ini terjadi belum diketahui.
- **G3.** Varian YOLO26 (Seg atau OBB) dan backbone regresi modern (mis. ConvNeXt, ViT) belum dibandingkan untuk pengukuran HC pada HC18.

## Langkah
1. **Protokol pencarian.** Tulis mesin atau situs yang benar-benar bisa kamu akses, rentang tahun 2018 sampai Oktober 2026, bahasa Inggris, kriteria inklusi (memakai HC18 untuk pengukuran HC atau segmentasi kepala janin) dan eksklusi (modalitas non-USG, biometri non-kepala, makalah tanpa pengenal yang bisa dilacak).
2. **Pencarian pembantah.** Jalankan minimal 10 query berbeda yang dirancang untuk menemukan kontra-contoh G1 dan G3, termasuk variasi berikut (tambahkan sendiri):
   - HC18 segmentation regression detection comparison
   - fetal head circumference YOLO OBB / oriented bounding box
   - fetal head circumference ConvNeXt / Vision Transformer regression
   - fetal head circumference ellipse detection one-stage
   - HC18 benchmark paradigms / unified protocol
   - HC18 patient-level split / grouped cross-validation / data leakage
3. **Kumpulkan kandidat.** Targetkan minimal 15 makalah yang memakai HC18. Setiap makalah harus benar-benar dibuka (teks lengkap bila bisa). Dilarang mengisi baris dari ingatan.
4. **Makalah yang wajib dibuka** (nama saja; temukan sendiri halaman dan isinya): Zhang dkk. 2020 (MIDL, regresi CNN); Zhang dkk. 2022 (J. Imaging, segmentation vs regression); Moccia, Fiorentino, Frontoni 2021 (Mask-R2CNN); "A regression framework to head-circumference delineation from US fetal images" (2021); RDHCformer (Front. Med. 2022); SAP-UNet (2025); "Ensemble transfer learning for fetal head analysis" (2022); Sobhaninia dkk. 2019 (arXiv:1909.00273); arXiv:2410.10352; arXiv:2604.18148; arXiv:2609.19230; arXiv:2603.26755; arXiv:2109.12474; van den Heuvel dkk. 2018.
5. **Tabel per makalah** dengan kolom: `No | Makalah | Paradigma (A, B, C, atau lainnya) | Dataset dan jumlah citra yang dipakai | Kalimat tentang split (maks 15 kata) dan lokasinya | Kategori split | Dievaluasi pada 335 citra uji resmi? | Augmentasi dilakukan sebelum split? | Metrik HC utama (nilai dan satuan) | URL | Status`.
   - Kategori split: `grouping-dinyatakan` | `acak-dinyatakan` | `split-dijelaskan-tanpa-grouping` | `uji-resmi-via-leaderboard` | `split-tidak-dijelaskan`.
   - Untuk "dievaluasi pada 335 citra uji resmi" dan "augmentasi sebelum split", isi `ya`, `tidak`, atau `tidak disebut`, selalu dengan kutipan bila `ya` atau `tidak`.
6. **Putusan tiap gap:** `SUPPORTED`, `WEAKENED`, atau `REFUTED`, dengan alasan yang hanya bersandar pada tabel dan search log.
   - G2: laporkan hitungan langsung dari tabel dalam bentuk "dari N makalah yang dibuka, K ...". Jangan memberi persentase bila N < 20. Makalah yang bukan studi HC18 atau memakai subset kecil dihitung terpisah dan diberi catatan.
   - G1 dan G3 adalah klaim negatif: statusnya `NOT-FOUND-IN-SEARCH` dengan daftar query. Tulis makalah terdekat dan apa yang membedakannya.
7. Tulis bagian Keterbatasan dan Usulan perubahan ke rencana (hanya usulan).
