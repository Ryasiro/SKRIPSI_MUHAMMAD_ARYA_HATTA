# data/

`hc18/` berisi dataset HC18 resmi dan **tidak di-commit** (lihat `.gitignore`). Struktur yang diharapkan:

```
data/hc18/
  training_set/                          999 citra + 999 anotasi (*_Annotation.png)
  test_set/                              335 citra (label tidak dibuka)
  training_set_pixel_size_and_HC.csv     filename, pixel size(mm), head circumference (mm)
  test_set_pixel_size.csv                filename, pixel size(mm)
```

Sumber: Zenodo, DOI 10.5281/zenodo.1322001. Jangan mengunduh dari sumber lain. Folder ini baca-saja bagi agent; turunan ditulis ke `data/hc18_derived*/`.

Jika kamu memindahkan folder kerja ke komputer lain atau ke Colab, unduh ulang dari Zenodo dan cocokkan jumlah berkas (2.333 PNG ditambah 2 CSV) sebelum menjalankan apa pun.
