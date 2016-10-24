import os
from flask_testing import TestCase
from create_app import create_app
from query_setoran import get_belum_setor
from setoran_models import *




class MyTest(TestCase):

    def create_app(self):
        app = create_app("flask_config.Testing")
        

        return app

    def setUp(self):
        # db.disconnect()
        db.create_tables()
        populate_db()


    def tearDown(self):
        db.drop_all_tables(with_all_data=True)
        os.remove("testing.sqlite")

    def test_index_has_context(self):
        """testing index, has this context:
                - sudah_setor
                - belum_setor
                - setoran, orderby tanggal, terbaru
        """
        self.client.get("/")
        sudah_setor = self.get_context_variable("sudah_setor")
        belum_setor = self.get_context_variable("belum_setor")
        setoran = self.get_context_variable("setoran")
        self.assertEqual(sudah_setor, "")
