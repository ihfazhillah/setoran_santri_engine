import os
import unittest
from query_setoran import get_belum_setor, get_belum_murojaah
from setoran_models import *

db.bind("sqlite", "testing.sqlite", create_db=True)
db.generate_mapping(create_tables=True)

class SetoranTest(unittest.TestCase):

    def assertListIn(self, expected_list, test_list):
        for expected in expected_list:
            self.assertIn(expected, test_list)

    def assertListNotIn(self, expected_list, test_list):
        for expected in expected_list:
            self.assertNotIn(expected, test_list)


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
                    timestamp=datetime.now(), lulus=False, santri=kholis)
            Setoran(start='1/1', end='1/7', jenis='tambah',
                    timestamp=datetime.now(), lulus=True, santri=suryadi)
            commit()


    def tearDown(self):
        db.drop_all_tables(with_all_data=True)
        os.remove("testing.sqlite")

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

    @db_session
    def test_yang_belum_setor_sama_sekali(self):
        blm_setor = get_belum_setor()
        self.assertEqual(count(blm_setor), 1)
        # self.fail(help(blm_setor))
        self.assertIn('raffi', [santri.nama for santri in blm_setor])
        self.assertNotIn('iqbal', [santri.nama for santri in blm_setor])

    @db_session
    def test_yang_belum_murojaah(self):
        blm_mur = get_belum_murojaah()
        self.assertEqual(count(blm_mur), 3)
        self.assertListIn(['raffi', 'suryadi', 'farhan'], [santri.nama for santri in blm_mur])

        self.assertListNotIn(['kholis', 'iqbal', 'wildan'],
                             [santri.nama for santri in blm_mur])
        
