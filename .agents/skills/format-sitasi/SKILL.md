---
name: format-sitasi
description: Aturan format IEEE (bawaan) dan APA 7 untuk daftar pustaka skripsi, termasuk dataset, repositori GitHub, dan preprint. Dipakai saat menyusun daftar pustaka dari klaim metadata yang sudah terverifikasi, atau saat pengguna bertanya aturan sitasi.
---

# Format sitasi

Bahan daftar pustaka hanya dari klaim metadata berstatus `VERIFIED-*` di catatan riset (penulis, tahun, judul, venue, volume, nomor, halaman, DOI). Metadata yang tidak terbaca di halaman sumber ditulis `[VERIFY]`, tidak diisi dari ingatan. DOI yang tidak tercatat di Log akses tidak dipakai.

## IEEE (bawaan)
- Di teks: angka dalam kurung siku sesuai urutan kemunculan pertama: `[1]`, `[2]`. Beberapa sumber: `[1], [3]` atau `[1]-[3]`.
- Jurnal: `[#] A. Penulis, B. Penulis, "Judul," Singkatan Jurnal, vol. X, no. Y, pp. Z-Z, Bulan Tahun, doi: ...`
- Prosiding: `[#] A. Penulis, "Judul," in Proc. Nama Konferensi, Kota, Tahun, pp. Z-Z.`
- Preprint: `[#] A. Penulis, "Judul," arXiv:XXXX.XXXXX, Tahun.`
- Situs: `[#] Penulis/Organisasi, "Judul," Nama Situs. [Online]. Available: URL. [Accessed: tanggal].`
- Dataset: `[#] A. Penulis, "Nama dataset" (versi), Platform, Tahun. doi: ... [Online]. Available: URL.`
- Repositori kode: penulis atau organisasi, nama repositori, tahun, URL, dan hash commit atau nomor rilis jika ketepatan versi penting (mis. Ultralytics dengan nomor versinya).

## APA 7 (jika program studi mewajibkan)
- Di teks: `(Penulis, Tahun)` atau `Penulis (Tahun)`.
- Jurnal: `Penulis, A. A. (Tahun). Judul artikel. Nama Jurnal, Volume(Nomor), halaman. https://doi.org/...`
- Prosiding: `Penulis, A. A. (Tahun). Judul. In Proceedings of ... (pp. xx-xx).`
- Preprint: `Penulis, A. A. (Tahun). Judul. arXiv. https://arxiv.org/abs/xxxx.xxxxx`

## Kasus khusus
- Preprint yang sudah terbit: kutip versi terbit; kutip preprint hanya jika memang versi paling relevan, dan beri label.
- Tanpa penulis perorangan: organisasi sebagai penulis.
- Tahun tidak diketahui: `n.d.`, bukan tebakan.
- Dataset HC18 dikutip dua sumber: makalah van den Heuvel et al., PLoS ONE, vol. 13, no. 8, e0200412, 2018, dan rekaman datanya di Zenodo (DOI 10.5281/zenodo.1322001; judul dan versi rekaman `[VERIFY]` sampai halaman Zenodo dibuka).

## Larangan
- Jangan mengarang DOI, halaman, atau volume. Biarkan `[VERIFY]` untuk diperiksa manual.
- Jangan memasukkan sumber yang belum dibuka dan diverifikasi.
