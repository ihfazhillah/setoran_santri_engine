import os
from flask_testing import TestCase
from flask import current_app
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

    @db_session
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
        belum_setor_from_db = get_belum_setor()
        sudah_setor_from_db = select(s for s in Santri if s not in belum_setor_from_db)
        setoran_from_db = select(s for s in Setoran).order_by(desc(Setoran.timestamp))[:5]
        self.assertEqual(list(belum_setor), list(belum_setor_from_db))
        self.assertEqual(list(sudah_setor), list(sudah_setor_from_db))
        self.assertEqual(list(setoran), list(setoran_from_db))


    @db_session
    def test_display_santri_id_one(self):
        """
        untuk sementara hanya menampilkan setoran santri yang berkaitan

            var :
                - setoran
        """
        self.client.get("/santri/display/1")
        setoran = self.get_context_variable("setoran")
        santri = self.get_context_variable("santri")
        setoran_from_db = select(s for s in Setoran if s.santri is santri)
        self.assertEqual(list(setoran), list(setoran_from_db))
        self.assertEqual(santri.nama, 'raffi')
        self.assertEqual(setoran.count(), 0)

    @db_session
    def test_display_santri_id_two(self):
        """
        sama seperti diatas, tapi hanya mengecek id 2
        """

        self.client.get("/santri/display/2")
        setoran = self.get_context_variable("setoran")
        santri = self.get_context_variable("santri")
        setoran_from_db = select(s for s in Setoran if s.santri is santri)
        self.assertEqual(setoran.count(), 1)
        self.assertEqual(santri.nama, "suryadi")
        self.assertEqual(list(setoran), list(setoran_from_db))

    def test_auth_login_page(self):
        resp = self.client.get("/auth/login")
        self.assert200(resp, "login page not found")
        login_form = self.get_context_variable('login_form')
        username = login_form.username
        password = login_form.password
        self.assertEqual(username.name, 'username')
        self.assertEqual(username.type, 'StringField')
        self.assertEqual(password.name, 'password')
        self.assertEqual(password.type, 'PasswordField')
        self.assertTrue(all(login_form.data[x] is None for x in login_form.data))

    def test_auth_login_page_with_post(self):
        resp = self.client.post("/auth/login", 
                                data={'username': 'username',
                                      'password': 'password'})
        self.assert_redirects(resp, "/")
        self.assert_message_flashed("Login Success")

    def test_auth_login_page_with_wrong_credential(self):
        resp = self.client.post("/auth/login",
                                data={'username': 'wrong_username',
                                      'password': 'wrong_password'})
        self.assert_message_flashed("Wrong username or password.", "warning")
        self.assert_200(resp)
        self.assert_template_used("auth/login.html")        


