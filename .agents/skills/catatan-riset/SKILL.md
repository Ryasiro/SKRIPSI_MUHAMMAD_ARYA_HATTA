---
name: catatan-riset
description: Format berkas catatan riset di research-notes/ dan aturan melanjutkan riset yang terputus antar-sesi. Dipakai oleh skill riset-literatur dan verifikasi-sumber, atau saat pengguna meminta melanjutkan riset yang sudah ada.
---

# Format catatan riset dan cara melanjutkan

Riset skripsi tidak selesai dalam satu sesi. Catatan di `research-notes/` adalah satu-satunya ingatan antar-sesi, jadi isinya harus cukup untuk dilanjutkan oleh agent lain yang tidak tahu apa pun.

## Penamaan
- `research-notes/<slug>.md`: catatan utama (huruf kecil, tanda hubung).
- `research-notes/<slug>.verifikasi.md`: hasil skill `verifikasi-sumber`.
- Skill `hc18-*` memakai nama tetap yang tertulis di skill masing-masing.
- Jangan menimpa berkas yang ada. Jika harus mengulang, tulis `<slug>-v2.md` dan sebutkan alasannya di frontmatter.

## Struktur
```markdown
---
topic: <pertanyaan riset lengkap>
status: draft | diverifikasi-agent | diaudit-manusia
tanggal-jalan: <YYYY-MM-DD>
last-updated: <YYYY-MM-DD>
model-agent: <nama model, bila diketahui>
ringkasan: <tiga kalimat, tanpa menilai kelulusan>
---

## Rencana
Sub-pertanyaan: tag, jenis, query penyangkal.

## Log akses
## Search log
## Tabel klaim
## Kemajuan per sub-pertanyaan
Status per sub-pertanyaan: `terjawab-bersumber` | `sumber-belum-terbuka` | `belum-terjawab`.

## Sintesis
Hanya dari klaim VERIFIED-*, tiap kalimat memuat ID klaim.

## Belum bisa dipakai
Klaim NOT-OPENED yang menunggu sumber.

## Celah
Klaim negatif dengan rujukan ke baris Search log.

## Keterbatasan
## Usulan perubahan ke rencana
## Keluaran lint
```

## Frontmatter untuk skill `hc18-*`
Skill `hc18-*` memakai `prompt-id` sebagai pengganti `topic` (lint menerima salah satunya). Contoh untuk P1:
```markdown
---
prompt-id: hc18-P1
status: draft
tanggal-jalan: <YYYY-MM-DD>
model-agent: <nama model, bila diketahui>
ringkasan: <tiga kalimat, tanpa menilai kelulusan>
---
```
Bagian wajib (Log akses, Search log, Tabel klaim, Keterbatasan, Usulan perubahan ke rencana, Keluaran lint) sama dengan struktur di atas. Skill `hc18-p4-data` yang menjalankan kode tidak punya Search log berisi pencarian web, tetapi lint tetap menuntut bagiannya: tulis satu baris `tidak ada pencarian web | - | <tanggal> | tidak tersedia | skill inspeksi data lokal`. Lint juga menuntut Tabel klaim di setiap catatan. Untuk P4, isi dengan temuan yang bersumber dari berkas atau dokumentasi yang dibuka (kolom `URL` boleh berupa jalur berkas lokal yang tercatat di Log akses); angka hasil eksekusi tetap disalin dari log di `research-notes/hc18-P4-log/`.

## Siapa boleh menulis `status`
- Agent penulis: hanya `draft`.
- Agent `verifikasi-sumber`: tidak mengubah status berkas aslinya.
- `diverifikasi-agent`: ditulis pengguna setelah seluruh tabel verifikasi selesai.
- `diaudit-manusia`: ditulis pengguna setelah memeriksa sendiri, atau setelah audit di luar workspace.

## Melanjutkan
1. Baca frontmatter dan status tiap sub-pertanyaan.
2. Kerjakan ulang hanya sub-pertanyaan `sumber-belum-terbuka` atau `belum-terjawab`.
3. Jangan mengulang pencarian atau pembukaan sumber yang sudah tercatat `VERIFIED-*`, kecuali pengguna meminta cek ulang.
4. Tambahkan baris baru ke log (jangan menghapus), perbarui `last-updated`, dan ulangi lint.
