from flask import Flask
from flask_testing import TestCase


class MyTest(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True 
        return app


    def test_index_has_context(self):
        """testing index, has this context:
                - sudah_setor
                - belum_setor
                - setoran, orderby tanggal, terbaru
        """
        self.client.get("/")
        self.get_context_variable("sudah_setor")
        self.get_context_variable("belum_setor")
        self.get_context_variable("setoran")
        