from datetime import datetime
from pony.orm import *


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
        raise ValueError

    return all(splitted.isdigit() for splitted in splitted_val)



class Santri(db.Entity):
    id = PrimaryKey(int, auto=True)
    nama = Required(str)
    setor = Required(bool, default=False)
    setorans = Set('Setoran', cascade_delete=True)


class Setoran(db.Entity):
    id = PrimaryKey(int, auto=True)
    start = Required(str, py_check=check_startend_format)
    end = Required(str, py_check=check_startend_format)
    jenis = Required(str)
    timestamp = Required(datetime)
    lulus = Required(bool)
    santri = Required(Santri)


# db.bind("sqlite", ":memory:")
# db.generate_mapping(create_tables=True)