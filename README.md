# ClipCraft

ClipCraft adalah aplikasi desktop untuk menyusun potongan teks yang sering digunakan. Tkinter menyediakan antarmuka, SQLite menyimpan modul teks secara lokal, dan pyperclip menyalin hasil ke clipboard sistem operasi.

## Fitur

- **Add** — menyimpan nama atau potongan teks sebagai modul.
- **Choose** — memilih modul yang telah tersimpan.
- **Load** — menambahkan modul terpilih ke akhir area teks.
- **Copy** — menyalin seluruh isi editor ke clipboard sistem.
- **Clear** — mengosongkan editor tanpa menghapus modul di database.
- **Delete** — menghapus modul yang sedang dipilih.

## Teknologi dan persyaratan

- Python 3 dengan Tkinter.
- SQLite melalui modul bawaan Python `sqlite3`.
- Paket Python `pyperclip`.

Pasang dependensi:

```bash
python -m pip install pyperclip
```

Tkinter biasanya disertakan pada instalasi Python untuk Windows. Pada beberapa distribusi Linux, Tkinter perlu dipasang menggunakan pengelola paket sistem.

## Menjalankan aplikasi

```bash
python ClipCraft.py
```

Aplikasi membuat `modules.db` jika belum tersedia. Database menyimpan daftar modul pada tabel `modules`. Karena path database bersifat relatif, jalankan aplikasi dari direktori kerja yang sama untuk menggunakan file database yang sama.

## Alur penggunaan

1. Masukkan teks pada kolom **Add New** dan tekan **Add**.
2. Pilih modul dari dropdown **Choose**.
3. Tekan **Load** untuk menambahkan teks tersebut ke editor. Teks yang sudah ada tetap dipertahankan dan modul baru ditambahkan pada baris berikutnya.
4. Tekan **Copy** untuk menyalin seluruh isi editor.
5. Tekan **Clear** untuk membersihkan editor saja.
6. Pilih modul dan tekan **Delete** untuk menghapus data modul tersebut.

## Penjelasan struktur kode

- `ClipboardApp.__init__`: menyiapkan koneksi SQLite, tabel, komponen GUI, dan penanganan penutupan.
- Metode `create_*`: membangun setiap bagian antarmuka secara terpisah.
- `get_module_list()`: membaca nama modul dari SQLite.
- `refresh_module_dropdown()`: memperbarui pilihan setelah data berubah.
- `add_module()` dan `delete_module()`: menambah dan menghapus data menggunakan parameter SQL.
- `load_from_database()`: mengambil modul yang dipilih dan menambahkannya ke editor.
- `copy_to_clipboard()`: menyalin editor menggunakan pyperclip.
- `clear_clipboard()`: menghapus isi editor tanpa mengubah database.
- `close_application()`: menutup cursor dan koneksi database saat jendela ditutup.

## Catatan audit

Komentar berbahasa Indonesia telah ditambahkan pada alur GUI, database, clipboard, dan entry point. Input modul kosong kini ditolak, pesan ditampilkan jika pengguna belum memilih modul, kegagalan clipboard ditangani, dan koneksi SQLite ditutup saat aplikasi berakhir. Skema database lama dipertahankan.

Pengujian GUI dan clipboard perlu dilakukan pada komputer desktop yang memiliki Tkinter serta dukungan clipboard sistem operasi.
