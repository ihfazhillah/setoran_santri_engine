from datetime import datetime
from pony.orm import *
import json 


db = Database()

def check_startend_format(val):
    """checking start_end value, 
    1. harus berupa string tapi isinya nomer
    2. dua value dipisah dengan /
    3. index[0] harus ada di data
    4. index[1] harus tidak boleh lebih dari jumlah ayat
    """
    splitted_val = val.split("/")

    if len(splitted_val) != 2:
        return False

    cur_surah = int(splitted_val[0])
    cur_ayah = int(splitted_val[1])

    all_digits = all(splitted.isdigit() for splitted in splitted_val)
    
    with open("daftar_surat.json") as f:
        daftar_surat = json.load(f, encoding="utf-8")

    all_surah_no = [surah['surah_no'] for surah in daftar_surat]

    surah_no = cur_surah in all_surah_no

    for surah in daftar_surat:
        if surah['surah_no'] == cur_surah:
            if cur_ayah > surah['surah_ayat']:
                return False
            if cur_ayah < 1:
                return False

    return all_digits and surah_no




class Santri(db.Entity):
    id = PrimaryKey(int, auto=True)
    nama = Required(str)
    setor = Required(bool, default=False)
    setorans = Set('Setoran', cascade_delete=True)


class Setoran(db.Entity):
    id = PrimaryKey(int, auto=True)
    start = Required(str, py_check=check_startend_format)
    end = Required(str, py_check=check_startend_format)
    jenis = Required(str, py_check=lambda v : v in ['tambah', 'murojaah'])
    timestamp = Required(datetime)
    lulus = Required(bool)
    santri = Required(Santri)


# db.bind("sqlite", ":memory:")
# db.generate_mapping(create_tables=True)