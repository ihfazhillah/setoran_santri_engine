


T_SANTRI, T_SANTRI_NAMA, SAVE_SANTRI, NO, T_SETORAN, T_SETORAN_NAMA, T_SETORAN_START, T_SETORAN_END, T_SETORAN_JENIS, T_SETORAN_SAVE, LHT_SANTRI, LHT_SURAT, LHT_FREE, LHT_BLM, LHT_BLM_SETOR, LHT_BLM_MUR, LHT_BLM_TAMBAH, LHT_BLM_MUR_ULANG, LHT_BLM_TAMBAH_ULANG = range(19)


reply_start = [KeyboardButton("👀 Lihat"), KeyboardButton("➕ Tambah")]
reply_persetujuan = [KeyboardButton("✔ Simpan"), KeyboardButton("✖ Jangan")]
reply_jenis = [KeyboardButton("➕ Tambah Baru"), KeyboardButton("♻ Murojaah")]
reply_lulus = [KeyboardButton("👍 Lulus"), KeyboardButton("👎 Ulang Lagi")]
reply_lihat = [[KeyboardButton("📃 Daftar Santri"), KeyboardButton("📚 Daftar Surat")],
[KeyboardButton("👏 Free"), KeyboardButton("⛔ Belum")]]
reply_belum = [[KeyboardButton("Setoran")],
               [KeyboardButton("♻ Murojaah"), KeyboardButton("➕ Tambah Baru")],
               [KeyboardButton("Murojaah sudah, harus ulang")],
               [KeyboardButton("Tambah sudah, harus ulang")]]