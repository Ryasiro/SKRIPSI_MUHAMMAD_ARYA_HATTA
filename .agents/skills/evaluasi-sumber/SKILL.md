---
name: evaluasi-sumber
description: Kriteria menilai apakah sebuah sumber akademik layak dikutip, termasuk pemeriksaan khusus makalah pencitraan medis (protokol split, kebocoran data, definisi metrik). Dipakai saat pengguna bertanya apakah suatu paper atau venue layak dikutip, atau saat riset-literatur dan verifikasi-sumber perlu menilai sumber.
---

# Evaluasi sumber

Penilaian di bawah hanya boleh ditulis dari halaman yang benar-benar dibuka dan tercatat di Log akses. Jika tidak terbuka, tulis `tidak diverifikasi`, bukan perkiraan.

## 1. Venue
Buka halaman jurnal, prosiding, atau indeks (SINTA untuk jurnal Indonesia, Scopus, DOAJ, DBLP) lalu catat apa yang tertulis di sana. Jangan menilai venue dari ingatan.

- **Kuat:** konferensi atau jurnal utama bidangnya; preprint (arXiv) boleh dikutip jika diberi label preprint dan belum ada versi terbit.
- **Hati-hati:** konferensi atau jurnal menengah; jurnal SINTA peringkat rendah; preprint tanpa tinjauan sejawat. Tulis labelnya saat mengutip.
- **Tanda bahaya:** tidak terindeks di mana pun; janji terbit cepat berbayar; nama menyerupai jurnal terkenal; tidak ada proses tinjauan sejawat yang dijelaskan; masuk daftar penerbit predator. Tulis temuan dan sarankan pengguna bertanya ke dosen pembimbing.
- Cek juga apakah halaman penerbit memuat pemberitahuan koreksi atau penarikan (retraction).

## 2. Pemeriksaan per makalah (umum)
- Apakah klaim di abstrak sesuai dengan yang didukung bagian metode dan hasil?
- Ukuran data wajar untuk klaimnya? Dibedakan jumlah citra, jumlah pemeriksaan, dan jumlah pasien?
- Apakah keterbatasan dibahas? Ketiadaan bagian keterbatasan adalah tanda bahaya kecil.
- Angka sitasi dan usia makalah hanya konteks, bukan alasan menolak.

## 3. Pemeriksaan tambahan untuk makalah pencitraan medis
Catat jawaban untuk setiap butir, atau `tidak dilaporkan` jika makalah tidak menyebutnya:
1. **Tingkat pemisahan data:** per citra, per pemeriksaan, atau per pasien? Apakah augmentasi dilakukan sebelum atau sesudah pemisahan?
2. **Set evaluasi:** set uji resmi (dengan label tersembunyi), validasi silang, atau sebagian data latih? Apakah set yang sama dipakai memilih model dan melaporkan hasil?
3. **Metrik:** definisi persis (MAE, MAD, selisih absolut rata-rata, selisih bertanda), satuan (mm atau piksel), dan apakah dilaporkan per citra atau per pasien.
4. **Pembanding:** apakah angka pembanding dari paper lain dihitung pada protokol yang sama? Jika tidak, perbandingan langsung tidak boleh disebut adil.
5. **Ketersediaan:** apakah kode atau bobot dirilis?

## 4. Sumber non-makalah
- Dokumentasi resmi atau spesifikasi: boleh untuk cara kerja teknis, bukan untuk klaim efektivitas.
- Blog vendor: konteks industri, tandai potensi bias.
- Blog pribadi atau Medium: hindari untuk skripsi kecuali satu-satunya sumber primer untuk hal yang sangat baru; tandai jelas.

## 5. Jika ragu
Tulis ketidakpastiannya, mis. "kredibilitas venue ini belum bisa dipastikan; sarankan tanya dosen pembimbing". Itu keluaran yang sah.
