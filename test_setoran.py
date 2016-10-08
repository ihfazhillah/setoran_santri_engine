import os
import unittest
from setoran_models import *


class SetoranTest(unittest.TestCase):


    def setUp(self):
        db.bind("sqlite", "testing.sqlite", create_db=True)
        db.generate_mapping(create_tables=True)

    def tearDown(self):
        os.remove("testing.sqlite")

    @db_session
    def test_start_end_format(self):
        """start or end harus berupa string, tapi dengan format 
        int/int
        misal 3/13
        """

        with self.assertRaises(ValueError):
            Setoran(start="hf", end='skdj', jenis='makan', timestamp=datetime.now()    , lulus=True, santri=Santri(nama='ihfazh'))

        with self.assertRaises(ValueError):
            Setoran(start="hf", end='skdj', jenis='makan', timestamp=datetime.now()    , lulus=True, santri=Santri(nama='ihfazh'))


        with self.assertRaises(ValueError):
            Setoran(start="hf/fs", end='jsfa/sdjfa', jenis='makan', timestamp=datetime.now()    , lulus=True, santri=Santri(nama='ihfazh'))


        Setoran(start="1/2", end='1/2', jenis='makan', timestamp=datetime.now()    , lulus=True, santri=Santri(nama='ihfazh'))
