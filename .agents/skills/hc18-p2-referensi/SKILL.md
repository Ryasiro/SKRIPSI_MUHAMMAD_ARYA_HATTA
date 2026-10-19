---
name: hc18-p2-referensi
description: Melengkapi dan memverifikasi metadata 25 referensi untuk skripsi HC18 (penulis lengkap, judul, venue, volume, halaman, DOI) langsung dari halaman penerbit atau repositori. Jalankan hanya jika pengguna mengetik /hc18-p2-referensi atau meminta P2 HC18 secara eksplisit.
---

# P2. Lengkapi dan verifikasi referensi

Ikuti Kontrak Output v2 di `AGENTS.md`. Keluaran: `research-notes/hc18-P2-referensi.md`.

## Cara kerja
Untuk setiap entri di bawah, buka halaman penerbit, resolver DOI, Crossref, PubMed, PMLR, atau arXiv dan baca sendiri metadatanya. Kolom "Pengenal" hanya petunjuk untuk menemukan karya itu. Pengenal bisa salah, jadi:
- Cek bahwa DOI mengarah ke judul yang sama dengan judul yang kamu cari. Jika berbeda, laporkan perbedaannya apa adanya.
- Tulis semua penulis sesuai urutan di halaman. Jangan menyingkat dengan "dkk." atau "et al." di tabel audit (singkatan hanya boleh di entri IEEE final bila penulis lebih dari enam).
- Entri tanpa pengenal: temukan sendiri. Jangan menebak venue. Jika versi jurnal atau konferensi tidak ditemukan, tulis `NOT-FOUND-IN-SEARCH` dengan query yang kamu jalankan.
- Satu karya, satu halaman bukti. Cantumkan URL halaman yang benar-benar kamu buka, bukan URL yang kamu duga.

## Daftar entri
| No | Karya | Pengenal (petunjuk, belum tentu benar) |
|---|---|---|
| 1 | Zhang dkk. 2020, "Direct estimation of fetal head circumference from ultrasound images based on regression CNN" | MIDL 2020, prosiding PMLR. Temukan halaman prosiding yang benar. |
| 2 | Zhang dkk. 2022, "Segmentation-based vs. regression-based biomarker estimation: a case study of fetus head circumference assessment from ultrasound images" | J. Imaging. Cari DOI. |
| 3 | RDHCformer (Front. Med. 2022) | doi 10.3389/fmed.2022.848904 |
| 4 | van den Heuvel dkk. 2018 (dataset HC18) | doi 10.1371/journal.pone.0200412; dataset Zenodo 10.5281/zenodo.1322001. Catat judul resmi persis seperti di halaman penerbit. |
| 5 | "Automatic measurement of head circumference in fetal ultrasound images using a squeeze atrous pooling UNet" (2025) | Cari venue, volume, nomor artikel, DOI. |
| 6 | Attention-ResUNet | arXiv:2604.18148 |
| 7 | "Open ultrasound foundation model for robust segmentation and clinical measurement across heterogeneous settings" | arXiv:2609.19230 |
| 8 | "Pubic symphysis-fetal head segmentation network using BiFormer attention mechanism and multipath dilated convolution" | arXiv:2410.10352. Apakah ada versi jurnal? |
| 9 | Domain-guided YOLO26 for fetal head ultrasound segmentation | arXiv:2603.26755. Catat nomor versi terbaru. |
| 10 | "Evolutionary techniques on fetal head segmentation" (2021) | Prosiding AIJR. Cari penulis, nama prosiding, halaman, DOI. |
| 11 | Mask-R2CNN (Moccia, Fiorentino, Frontoni, 2021) | doi 10.1007/s11548-021-02430-0 |
| 12 | "A regression framework to head-circumference delineation from US fetal images" (2021) | Cari penulis (urutan!), jurnal, volume, nomor artikel, DOI. |
| 13 | "Ensemble transfer learning for fetal head analysis: from segmentation to gestational age and weight prediction" (2022) | Cari penulis, jurnal, volume, nomor artikel, DOI. |
| 14 | "A multicentre benchmark dataset for comprehensive landmark-based fetal ultrasound biometry" (2026) | doi 10.1038/s41598-026-47854-3. Berkas `41598_2026_Article_47854.pdf` mungkin ada di folder proyek. |
| 15 | ISUOG Practice Guidelines: ultrasound assessment of fetal biometry and growth (2019) | DOI yang diduga 10.1002/uog.20272. Verifikasi. DOI 10.1002/uog.19029 dilarang. |
| 16 | INTERGROWTH-21st, Fetal Growth Longitudinal Study (Lancet 2014) | doi 10.1016/S0140-6736(14)61490-2 |
| 17 | EllipseNet: anchor-free ellipse detection for automatic cardiac biometrics in fetal echocardiography | arXiv:2109.12474. Cari versi konferensi. Jangan menebak venue. |
| 18 | Taha dan Hanbury, metrics for evaluating 3D medical image segmentation (2015) | doi 10.1186/s12880-015-0068-x |
| 19 | Bland dan Altman, statistical methods for assessing agreement between two methods of clinical measurement (1986) | doi 10.1016/S0140-6736(86)90837-8 |
| 20 | Bland dan Altman, measuring agreement in method comparison studies (1999) | doi 10.1177/096228029900800204 |
| 21 | Checklist for Artificial Intelligence in Medical Imaging (CLAIM) | doi 10.1148/ryai.2020200029 |
| 22 | TRIPOD+AI statement (2024) | doi 10.1136/bmj-2023-078378 |
| 23 | Sobhaninia dkk., "Fetal ultrasound image segmentation for measuring biometric parameters using multi-task deep learning" | arXiv:1909.00273. Cari venue dan tahun terbit definitif. |
| 24 | Dataset anotasi kepala janin skala besar dari Alzubaidi dkk. (Data in Brief, 2023) | Judul diduga "Large-scale annotation dataset for fetal head biometry in ultrasound images". Verifikasi judul, penulis, DOI. |
| 25 | Ultralytics YOLO26 | Halaman dokumentasi resmi YOLO26 dan makalah yang dikutip oleh halaman itu. Catat URL dan tanggal akses. |

## Keluaran
1. Tabel per entri: `No | field | nilai yang kamu baca | status | URL halaman yang kamu buka`. Satu baris per field yang kamu cek (penulis, judul, venue, volume, nomor, halaman, tahun, DOI).
2. Daftar entri IEEE final. Field yang tidak terkonfirmasi ditulis `[VERIFY]`, dan jangan diisi dengan tebakan.
3. Daftar ketidakcocokan: pengenal di tabel di atas yang ternyata salah atau mengarah ke karya lain, lengkap dengan apa yang sebenarnya kamu temukan.
