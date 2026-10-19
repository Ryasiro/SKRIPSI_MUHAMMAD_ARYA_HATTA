---
name: hc18-p1-novelty
description: Menguji tiga hipotesis research gap HC18 (loss berbasis kontur pada U-Net, split tanpa grouping, pelaporan metrik batas dan galat HC) lewat pencarian literatur dan tabel per makalah. Jalankan hanya jika pengguna mengetik /hc18-p1-novelty atau meminta P1 HC18 secara eksplisit.
---

# P1. Uji novelty tiga hipotesis gap

Ikuti Kontrak Output v2 di `AGENTS.md`. Keluaran: `research-notes/hc18-P1-novelty.md`.

Judul dan konteks skripsi ada di bagian Konteks `AGENTS.md`. Tabel per makalah (langkah 5) adalah matriks deskriptif. Tabel klaim dari Kontrak tetap ditulis terpisah sebagai tempat bukti (langkah 6).

## Hipotesis (tugasmu mencoba membantahnya, bukan mengonfirmasinya)
- **G1.** Tidak ada makalah yang membandingkan fungsi loss berbasis kontur (contoh: boundary loss, Hausdorff-distance loss, active contour loss) dengan loss berbasis region (Dice, cross-entropy) pada U-Net untuk segmentasi kepala janin pada HC18, dalam satu protokol yang sama dan dengan galat HC (mm) sebagai keluaran.
- **G2.** Set uji HC18 tidak berlabel publik, sehingga banyak studi membagi ulang 999 citra latih. Sebagian mungkin membagi tanpa grouping per pemeriksaan. Seberapa sering hal ini terjadi belum diketahui.
- **G3.** Studi segmentasi HC18 umumnya melaporkan metrik overlap (Dice, IoU). Berapa banyak yang juga melaporkan metrik batas (HD, HD95, ASSD) dan galat HC (mm) belum diketahui.

## Langkah
1. **Protokol pencarian.** Tulis mesin atau situs yang benar-benar bisa kamu akses, rentang tahun 2018 sampai Oktober 2026, bahasa Inggris, kriteria inklusi (memakai HC18 untuk pengukuran HC atau segmentasi kepala janin) dan eksklusi (modalitas non-USG, biometri non-kepala, makalah tanpa pengenal yang bisa dilacak). Makalah loss berbasis kontur di domain lain (CT, MRI, citra alam) tidak dihitung untuk G1 dan G2; catat terpisah sebagai bahan landasan teori.
2. **Pencarian pembantah.** Jalankan minimal 10 query berbeda yang dirancang untuk menemukan kontra-contoh G1, G2, dan G3, termasuk variasi berikut (tambahkan sendiri):
   - HC18 boundary loss fetal head segmentation
   - Hausdorff distance loss fetal ultrasound segmentation
   - active contour loss ultrasound segmentation
   - distance transform / signed distance map loss fetal head
   - fetal head circumference U-Net loss function comparison
   - HC18 Dice loss versus boundary loss head circumference error
   - HC18 segmentation HD95 / Hausdorff head circumference
   - HC18 patient-level split / grouped cross-validation / data leakage
3. **Kumpulkan kandidat.** Targetkan minimal 15 makalah yang memakai HC18. Setiap makalah harus benar-benar dibuka (teks lengkap bila bisa). Dilarang mengisi baris dari ingatan.
4. **Makalah yang wajib dibuka** (nama saja; temukan sendiri halaman dan isinya): Zhang dkk. 2020 (MIDL, regresi CNN); Zhang dkk. 2022 (J. Imaging, segmentation vs regression); Moccia, Fiorentino, Frontoni 2021 (Mask-R2CNN); "A regression framework to head-circumference delineation from US fetal images" (2021); RDHCformer (Front. Med. 2022); SAP-UNet (2025); "Ensemble transfer learning for fetal head analysis" (2022); Sobhaninia dkk. 2019 (arXiv:1909.00273); arXiv:2410.10352; arXiv:2604.18148; arXiv:2609.19230; arXiv:2603.26755; arXiv:2109.12474 (rancangan lama, bukan studi HC18: hitung terpisah); van den Heuvel dkk. 2018.

   **Petunjuk topik loss berbasis kontur** (nama dan tahun adalah petunjuk penyusun skill, belum diverifikasi; temukan sendiri halaman primernya): Kervadec dkk., boundary loss (versi MIDL 2019 dan versi jurnal); Karimi dan Salcudean, Hausdorff distance loss (jurnal, 2020); Chen dkk., active contour loss (CVPR 2019); Caliva dkk., distance map loss penalty term (MIDL 2019); Ma dkk., "Loss odyssey in medical image segmentation" (2021). Karya ini masuk landasan teori, bukan hitungan G1 atau G2, kecuali ia memakai HC18 atau segmentasi kepala janin.
5. **Tabel per makalah** dengan kolom: `No | Makalah | Pendekatan (segmentasi, regresi, deteksi, atau lainnya) | Arsitektur dan fungsi loss (persis seperti di makalah) | Dataset dan jumlah citra yang dipakai | Kalimat tentang split (maks 15 kata) dan lokasinya | Kategori split | Dievaluasi pada 335 citra uji resmi? | Augmentasi dilakukan sebelum split? | Metrik overlap (Dice atau IoU, nilai) | Metrik batas (HD, HD95, ASSD) dilaporkan? | Galat HC utama (nilai dan satuan) | URL | Status`.
   - Kategori split: `grouping-dinyatakan` | `acak-dinyatakan` | `split-dijelaskan-tanpa-grouping` | `uji-resmi-via-leaderboard` | `split-tidak-dijelaskan`.
   - Untuk "dievaluasi pada 335 citra uji resmi", "augmentasi sebelum split", dan "metrik batas dilaporkan", isi `ya`, `tidak`, atau `tidak disebut`, selalu dengan kutipan bila `ya` atau `tidak`.
   - Kolom `Status` memakai status Kontrak (`VERIFIED-PRIMARY`, `VERIFIED-SECONDARY`, `NOT-OPENED`).
6. **Tabel klaim dan putusan tiap gap.** Tabel klaim Kontrak memuat satu baris per putusan G1 sampai G3, dan satu baris per makalah untuk angka utamanya (galat HC dan metrik batas) dengan kutipan serta lokasi bukti. Putusan: `SUPPORTED`, `WEAKENED`, atau `REFUTED`, dengan alasan yang hanya bersandar pada tabel dan search log.
   - G2: laporkan hitungan langsung dari tabel dalam bentuk "dari N makalah yang dibuka, K ...". Jangan memberi persentase bila N < 20. Makalah yang bukan studi HC18 atau memakai subset kecil dihitung terpisah dan diberi catatan.
   - G3: laporkan "dari N makalah segmentasi yang dibuka, K melaporkan metrik batas, M melaporkan galat HC (mm), L melaporkan keduanya". Jangan memberi persentase bila N < 20.
   - G1 adalah klaim negatif: statusnya `NOT-FOUND-IN-SEARCH` dengan daftar query. Tulis makalah terdekat dan apa yang membedakannya (loss yang dibandingkan, dataset, protokol split, ada tidaknya galat HC).
7. Tulis bagian Keterbatasan dan Usulan perubahan ke rencana (hanya usulan).
