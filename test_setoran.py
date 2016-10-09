#pylint: disable=w0614, w0401, w0622, E1123
import os
import unittest
from datetime import timedelta
from query_setoran import get_belum_setor, get_belum_murojaah, get_sudah_tambah_harus_ulang, get_sudah_murojaah_harus_ulang, get_sudah_free
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
        populate_db()


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
                Setoran(start="hf", end='skdj', jenis='makan', timestamp=datetime.now(), lulus=True, santri=Santri(nama='ihfazh'))

            with self.assertRaises(ValueError):
                Setoran(start="hf", end='skdj', jenis='makan', timestamp=datetime.now(), lulus=True, santri=Santri(nama='ihfazh'))


            with self.assertRaises(ValueError):
                Setoran(start="hf/fs", end='jsfa/sdjfa', jenis='makan', timestamp=datetime.now(), lulus=True, santri=Santri(nama='ihfazh'))


            Setoran(start="1/2", end='1/2', jenis='tambah', timestamp=datetime.now(), lulus=True, santri=Santri(nama='ihfazh'))

    @db_session
    def test_startend_data_notfound(self):
        with self.assertRaises(ValueError):
            Setoran(start="300/2", end='0/2', jenis='makan', timestamp=datetime.now(), lulus=True, santri=Santri(nama='ihfazh'))

        Setoran(start="1/2", end="1/3", jenis='tambah', timestamp=datetime.now(), lulus=True, santri=Santri(nama='ihfazh'))

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
        # self.assertEqual(count(blm_mur), 3)
        self.assertListIn(['raffi', 'suryadi', 'farhan'], [santri.nama for santri in blm_mur])

        self.assertListNotIn(['kholis', 'iqbal', 'wildan'],
                             [santri.nama for santri in blm_mur])
        
    @db_session
    def test_yang_sudah_tambah_harus_ulang(self):
        tambah_ulang = get_sudah_tambah_harus_ulang()
        self.assertEqual(count(tambah_ulang), 1)
        self.assertIn('suryadi', [santri.nama for santri in tambah_ulang])
        self.assertListNotIn(['wildan', 'iqbal', 'farhan', 'kholis' 'raffi'],
                             [santri.nama for santri in tambah_ulang])

    @db_session
    def test_sudah_murojaah_tapi_harus_ulang(self):
        mur_ulang = get_sudah_murojaah_harus_ulang()
        self.assertEqual(count(mur_ulang), 1)
        list_hasil = [santri.nama for santri in mur_ulang]
        self.assertIn('iqbal', list_hasil)
        self.assertListNotIn(['suryadi', 'wildan', 
                              'farhan', 'kholis', 'raffi'], list_hasil)

    @db_session
    def test_sudah_tidak_ada_tanggungan(self):
        free = get_sudah_free()
        list_hasil = [santri.nama for santri in free]
        self.assertEqual(count(free), 1)
        self.assertIn('wildan', list_hasil)
        self.assertListNotIn(['suryadi', 'iqbal', 
                              'farhan', 'kholis', 'raffi'], list_hasil)

    @db_session
    def test_yang_belum_murojaah_tambah_sama_sekali_hari_ini(self):
        """ditest ini dan yang berikutnya, akan menambahkan setoran dihari yang kemarin dan dia sudah tidak ada tanggungan dihari kemarin.

        result adalah hanya santri yang belum setor hari ini..."""
        raffi = get(santri for santri in Santri if santri.nama == 'raffi')
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        Setoran(start='1/1', end='1/3', jenis='tambah', lulus=True, timestamp=yesterday, santri=raffi)
        Setoran(start='1/1', end='1/3', jenis='murojaah', lulus=True, timestamp=yesterday, santri=raffi)
        blm = get_belum_setor()
        self.assertEqual(count(blm), 1)
        self.assertIn('raffi', [santri.nama for santri in blm])

    @db_session
    def test_yang_belum_murojaah_hari_ini(self):
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        suryadi = get(santri for santri in Santri if santri.nama == 'suryadi')
        farhan = get(santri for santri in Santri if santri.nama == 'farhan')
        Setoran(start='1/1', end='2/3', jenis='murojaah', lulus=True,
                timestamp=yesterday, santri=suryadi)
        Setoran(start='1/1', end='2/3', jenis='murojaah', lulus=True,
                timestamp=yesterday, santri=farhan)
        commit()
        blm = get_belum_murojaah()
        list_belum = [santri.nama for santri in blm]
        # self.assertEqual(count(blm), 3)
        self.assertListIn(['suryadi', 'raffi', 'farhan'], list_belum)
        self.assertNotIn(['iqbal', 'wildan', 'kholis'], list_belum)
