import os
import unittest
from setoran_models import *


db.bind("sqlite", "testing.sqlite", create_db=True)
db.generate_mapping(create_tables=True)

class SetoranTest(unittest.TestCase):


    def setUp(self):
        # db.disconnect()
        db.create_tables()

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


            Setoran(start="1/2", end='1/2', jenis='makan', timestamp=datetime.now()    , lulus=True, santri=Santri(nama='ihfazh'))

    @db_session
    def test_startend_data_notfound(self):
        with self.assertRaises(ValueError):
            Setoran(start="300/2", end='0/2', jenis='makan', timestamp=datetime.now()    , lulus=True, santri=Santri(nama='ihfazh'))



    
   
