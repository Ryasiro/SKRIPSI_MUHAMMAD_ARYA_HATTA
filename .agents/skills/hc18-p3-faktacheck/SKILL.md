---
name: hc18-p3-faktacheck
description: Memeriksa fakta dataset HC18, angka dari literatur segmentasi dan loss berbasis kontur, serta makna grup nama file untuk validasi berbasis subjek, langsung dari sumber primer, dalam bentuk pertanyaan tanpa nilai harapan. Jalankan hanya jika pengguna mengetik /hc18-p3-faktacheck atau meminta P3 HC18 secara eksplisit.
---

# P3. Fact-check lewat pertanyaan terbuka

Ikuti Kontrak Output v2 di `AGENTS.md`. Keluaran: `research-notes/hc18-P3-faktacheck.md`.

Pertanyaan D1 sampai D8 dan L1 sampai L9 diprioritaskan untuk judul skripsi yang baru. D6 dan D7 menentukan apakah kata "subjek" pada judul boleh dipakai apa adanya (lihat aturan kerja 5 di `AGENTS.md`). Pertanyaan L10, L11, T1, dan T2 berasal dari rancangan lama (YOLO26, OBB, deteksi elips); kerjakan paling akhir dan hanya jika pengguna memintanya. Pertanyaan L15 sampai L20 ditambahkan untuk topik loss berbasis kontur.

Tidak ada nilai yang "diharapkan" di sini. Jawab setiap pertanyaan dengan nilai yang kamu baca sendiri di sumber, lengkap dengan lokasi dan kutipan. Jika tabel atau gambar tidak terbaca, status `NOT-OPENED`. Jangan menebak isi tabel.

Untuk tiap angka dari literatur, catat juga protokol evaluasinya: dataset, jumlah citra, set evaluasi (uji resmi, validasi internal, atau lainnya), dan cara split bila disebut.

## A. Dataset HC18 (paper van den Heuvel dkk., halaman dataset Zenodo, halaman grand-challenge HC18)
- **D1.** Jumlah citra latih dan uji, ukuran piksel citra, rentang ukuran piksel (mm per piksel). Sebutkan per sumber, karena sumber bisa berbeda.
- **D2.** Bagaimana citra dibagi menjadi latih dan uji? Kutip kalimatnya.
- **D3.** Apakah label citra uji dirilis? Apakah pengiriman hasil ke leaderboard grand-challenge masih terbuka? Format berkas submisi (kolom), metrik yang ditampilkan, dan tanggal submisi terbaru yang tampak di tab Results (bila tab terbuka tanpa login).
- **D4.** Kolom apa saja di CSV publik? Apakah ada usia gestasi?
- **D5.** Bagaimana label latih dibuat (siapa, bagaimana)? Apa yang dikatakan tentang bentuk dan ketebalan anotasi? Sebutkan per sumber, karena paper dan halaman dataset bisa berbeda.
- **D6.** Apakah dokumentasi resmi menjelaskan arti angka di awal nama file? Apakah ada kalimat yang menghubungkannya dengan pemeriksaan atau pasien?
- **D7.** Berapa jumlah perempuan atau pemeriksaan yang disebut paper? Apa kriteria inklusi dan eksklusi subjek (mis. janin abnormal)?
- **D8.** Metrik apa saja yang dilaporkan van den Heuvel dkk. untuk metode otomatis terhadap pengamat 1, dan untuk pengamat 2 terhadap pengamat 1 (mean difference, SD, limits of agreement, absolute difference)? Kutip angka dari teks. Jika angka ada di tabel berupa gambar yang tidak terbaca, status `NOT-OPENED`.

## B. Literatur (angka beserta protokolnya)
- **L1.** SAP-UNet (2025): DSC, Hausdorff, selisih HC (rata-rata dan absolut), dataset, split.
- **L2.** Attention-ResUNet (arXiv:2604.18148): Dice yang dilaporkan, jumlah sampel (n), split.
- **L3.** Ensemble transfer learning (2022): mIoU, MAD, dataset, jumlah citra, urutan augmentasi dan split, set tempat angka utama dihitung.
- **L4.** Mask-R2CNN (2021): angka MAD di abstrak; pada set apa angka itu dievaluasi; berapa citra validasi; adakah pengiriman ke platform tantangan.
- **L5.** "A regression framework to head-circumference delineation from US fetal images": MAD, DSC, set evaluasi.
- **L6.** RDHCformer (2022): MAE dan ME beserta SD, set evaluasi, jumlah citra latih dan validasi setelah augmentasi, serta apa yang paper katakan tentang arsitektur (satu tahap? anchor-free? post-processing?).
- **L7.** Zhang dkk. 2020 (MIDL): arsitektur dan loss terbaik, metrik terbaik, cara split, apakah grouping per pemeriksaan disebut (baca PDF, bukan hanya abstrak).
- **L8.** Zhang dkk. 2022 (J. Imaging): jumlah citra latih, validasi, uji; acak atau tidak; ada tidaknya cross-validation; metrik terbaik untuk pendekatan segmentasi dan regresi; arsitektur yang dipakai; kesimpulan penulis.
- **L9.** SonoBase (arXiv:2609.19230): error HC per konfigurasi (box prompt, point prompt) dan baseline, "ellipse-fitting floor" (nilai dan lokasi definisinya), n dan dataset, serta sumber angka variabilitas antar-pengamat yang dikutip.
- **L10.** (rancangan lama) Nizar (arXiv:2603.26755): dataset yang dipakai (nama, jumlah citra), kelas, apakah HC diukur, varian YOLO26, cara split, jumlah citra uji, metrik utama, baseline, dan apakah perbandingan keduanya sebanding menurut paper.
- **L11.** (rancangan lama) EllipseNet (arXiv:2109.12474): apa yang dikatakan tentang regresi langsung parameter elips (kutip kalimat dan bagian), tugas dan dataset aslinya, venue.
- **L12.** Di Vece dkk. 2026: jumlah citra, subjek, perangkat, dan situs klinik; sumber data; bagaimana landmark untuk subset HC18 diperoleh; lisensi. Baca `41598_2026_Article_47854.pdf` bila ada di folder proyek.
- **L13.** Sobhaninia dkk. 2019 (arXiv:1909.00273): dataset, split, hasil HC (bila ada angka).
- **L14.** arXiv:2410.10352: dataset yang dipakai, cara split, metrik; apakah HC dihitung.

- **L15.** Kervadec dkk., boundary loss: definisi loss (rumus dan nomor persamaan), apakah dipakai sebagai pengganti atau tambahan pada loss region, jadwal bobot antar-loss yang dipakai, dataset dan metrik yang dilaporkan, apakah metrik batas dilaporkan. Baca teks lengkap, bukan hanya abstrak.
- **L16.** Karimi dan Salcudean, Hausdorff distance loss: tiga pendekatan yang diusulkan (nama persis di paper), dataset, metrik yang dilaporkan (HD, Dice), serta apakah perkiraan HD dipakai bersama loss lain.
- **L17.** Chen dkk., active contour loss: komponen loss (panjang kontur, region), dataset, metrik, dan apakah ada pengaturan bobot antar-komponen.
- **L18.** Caliva dkk., distance map loss penalty: bentuk penalti, dataset, metrik, dan apakah dipakai bersama loss region.
- **L19.** Ma dkk., "Loss odyssey": daftar loss yang dibandingkan dan kategorinya menurut paper, dataset, metrik, serta kesimpulan penulis tentang loss mana yang konsisten lebih baik (kutip kalimatnya).
- **L20.** Dari SAP-UNet, Attention-ResUNet, dan makalah segmentasi HC18 lain yang kamu buka: fungsi loss apa yang dipakai (nama persis), apakah ada komponen berbasis kontur atau jarak, dan apakah HD atau HD95 dilaporkan.

## C. Teknis
- **T1.** (rancangan lama) Dokumentasi resmi Ultralytics YOLO26: task apa saja yang didukung, nama bobot pralatih per task (khususnya OBB bila ada), tanggal rilis. Catat URL dan tanggal halaman.
- **T2.** (rancangan lama) Spesifikasi format label YOLO OBB di dokumentasi Ultralytics (jumlah nilai per baris, urutan titik, normalisasi koordinat).
- **T3.** Dokumentasi resmi pustaka yang dipakai untuk fit elips (OpenCV `fitEllipse`): apa yang dikembalikan (pusat, sumbu penuh atau setengah, sudut), dan satuan sudutnya. Catat URL dan versi dokumentasi. Rumus keliling Ramanujan: baca sumber primernya atau tulis `NOT-OPENED`.

## Keluaran
Tabel `ID | pertanyaan | nilai di sumber | URL | lokasi bukti | kutipan (maks 15 kata) | status | catatan`, lalu bagian "Hal yang tampak bertentangan antar sumber", Keterbatasan, dan Usulan perubahan ke rencana.
