import os
import unittest
from setoran_models import *


db.bind("sqlite", "testing.sqlite", create_db=True)
db.generate_mapping(create_tables=True)

class SetoranTest(unittest.TestCase):


    def setUp(self):
        # db.disconnect()
        db.create_tables()
        with db_session:
            raffi = Santri(nama='raffi')
            suryadi = Santri(nama='suryadi')
            kholis = Santri(nama='kholis')
            farhan = Santri(nama='farhan')
            iqbal = Santri(nama='iqbal')
            wildan = Santri(nama='wildan')
            Setoran(start='1/1', end='1/7', jenis='murojaah',
                    timestamp=datetime.now(), lulus=True, santri=wildan)
            Setoran(start='1/1', end='1/7', jenis='tambah',
                    timestamp=datetime.now(), lulus=True, santri=wildan)
            Setoran(start='1/1', end='1/7', jenis='murojaah',
                    timestamp=datetime.now(), lulus=False, santri=iqbal)
            Setoran(start='1/1', end='1/7', jenis='tambah',
                    timestamp=datetime.now(), lulus=True, santri=farhan)
            Setoran(start='1/1', end='1/7', jenis='murojaah',
                    timestamp=datetime.now(), lulus=True, santri=kholis)
            Setoran(start='1/1', end='1/7', jenis='tambah',
                    timestamp=datetime.now(), lulus=True, santri=farhan)
            commit()


    def tearDown(self):
        db.drop_all_tables(with_all_data=True)
        os.remove("testing.sqlite")
        pass

    def test_start_end_format(self):
        """start or end harus berupa string, tapi dengan format 
        int/int
        misal 3/13
        """
        with db_session():
            with self.assertRaises(ValueError):
                Setoran(start="hf", end='skdj', jenis='makan', timestamp=datetime.now()    , lulus=True, santri=Santri(nama='ihfazh'))

            with self.assertRaises(ValueError):
                Setoran(start="hf", end='skdj', jenis='makan', timestamp=datetime.now()    , lulus=True, santri=Santri(nama='ihfazh'))


            with self.assertRaises(ValueError):
                Setoran(start="hf/fs", end='jsfa/sdjfa', jenis='makan', timestamp=datetime.now()    , lulus=True, santri=Santri(nama='ihfazh'))


            Setoran(start="1/2", end='1/2', jenis='tambah', timestamp=datetime.now()    , lulus=True, santri=Santri(nama='ihfazh'))

    @db_session
    def test_startend_data_notfound(self):
        with self.assertRaises(ValueError):
            Setoran(start="300/2", end='0/2', jenis='makan', timestamp=datetime.now()    , lulus=True, santri=Santri(nama='ihfazh'))

        Setoran(start="1/2", end="1/3", jenis='tambah', timestamp=datetime.now(),
            lulus=True, santri=Santri(nama='ihfazh'))

    @db_session
    def test_startend_ayat_data_not_lt_or_not_gt_surah_ayat(self):
        """ayat yang dicatat tidak boleh lebih banyak atau lebih sedikit
        daripada ayatnya surat yang di tulis"""

        with self.assertRaises(ValueError):
            Setoran(start="1/0", end='1/10', jenis='makan', timestamp=datetime.now(), lulus=True, santri=Santri(nama='ihfazh'))

        with self.assertRaises(ValueError):
            Setoran(start="1/0", end='1/6', jenis='makan', timestamp=datetime.now(), lulus=True, santri=Santri(nama='ihfazh'))

        Setoran(start="1/1", end='1/7', jenis='tambah', timestamp=datetime.now(), lulus=True, santri=Santri(nama='ihfazh'))


    @db_session
    def test_jenis_hanya_boleh_dua(self):
        """yaitu murojaah dan tambah"""

        with self.assertRaises(ValueError):
            Setoran(start="1/1", end='1/6', jenis='makan', timestamp=datetime.now(), lulus=True, santri=Santri(nama='ihfazh'))

        Setoran(start="1/1", end='1/6', jenis='tambah', timestamp=datetime.now(), lulus=True, santri=Santri(nama='ihfazh'))
        Setoran(start="1/1", end='1/6', jenis='murojaah', timestamp=datetime.now(), lulus=True, santri=Santri(nama='ihfazh'))


