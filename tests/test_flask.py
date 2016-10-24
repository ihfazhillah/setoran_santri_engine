from flask import Flask, render_template
from flask_testing import TestCase
from create_app import create_app


class MyTest(TestCase):

    def create_app(self):
        app = create_app("flask_config.Testing")
        

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
