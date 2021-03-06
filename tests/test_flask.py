import os
from flask_testing import TestCase
from create_app import create_app
from query_setoran import get_belum_setor
from setoran_models import db, populate_db, Santri, Setoran
from pony.orm import db_session, select, get, desc


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

    def login(self):
        resp = self.client.post("/auth/login", data={'username': 'username',
                                                     'password': 'password'})
        self.assert_redirects(resp, "/")

    def logout(self):
        resp = self.client.get("/auth/logout")
        self.assert_message_flashed("Logout success.")
        self.assert_redirects(resp, "/")

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
        sudah_setor_from_db = select(s for s in Santri
                                     if s not in belum_setor_from_db)
        setoran_from_db = select(s for s in Setoran
                                 ).order_by(desc(Setoran.timestamp))[:5]
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
        self.assertTrue(all(login_form.data[x] is None
                            for x in login_form.data))

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

    def test_aut_login_page_with_incorrect_password(self):
        resp = self.client.post("/auth/login",
                                data={'username': 'username',
                                      'password': 'wrong_password'})
        self.assert_message_flashed("Wrong username or password.", "warning")
        self.assert200(resp)
        self.assert_template_used("auth/login.html")

    def test_auth_logout_without_login(self):
        resp = self.client.get("/auth/logout")
        self.assert_redirects(resp, "/auth/login?next=%2Fauth%2Flogout")
        self.assert_message_flashed("You're not logged in", "warning")

    def test_auth_logout_with_login(self):
        self.login()
        self.logout()

    def test_delete_santri_without_login(self):
        resp = self.client.get("/santri/delete/1")
        self.assert_redirects(resp, "/auth/login?next=%2Fsantri%2Fdelete%2F1")
        self.assert_message_flashed("You're not logged in", "warning")

    def test_delete_santri_after_login(self):
        self.login()
        resp = self.client.get("/santri/delete/1")
        self.assert_redirects(resp, "/")
        self.assert_message_flashed("Santri with id 1 was removed.", "info")
        with db_session:
            santries = select(s for s in Santri)
            self.assertEqual(santries.count(), 5)
            self.assertNotIn("raffi", [s.nama for s in santries])

    def test_edit_santri_without_login(self):
        resp = self.client.post("/santri/edit/1",
                                data={"nama": "ihfazh"})
        self.assert_redirects(resp, "/auth/login?next=%2Fsantri%2Fedit%2F1")
        self.assert_message_flashed("You're not logged in", "warning")

    def test_edit_santri_after_login(self):
        self.login()
        resp = self.client.post("/santri/edit/1",
                                data={"nama": "ihfazh"})
        self.assert_redirects(resp, "/")
        self.assert_message_flashed("Santri with id 1 was edited.", "info")
        with db_session:
            santri = select(s for s in Santri)
            self.assertEqual(santri.count(), 6)
            ihfazh = get(s for s in Santri if s.id == 1)
            self.assertEqual(ihfazh.nama, "ihfazh")

    def test_edit_santri_and_empty_nama_field(self):
        self.login()
        resp = self.client.post("/santri/edit/1",
                                data={'nama': ''})
        self.assert_redirects(resp, "/")
        with db_session:
            santri = select(s for s in Santri)
            self.assertEqual(santri.count(), 6)
            raffi = get(s for s in Santri if s.id == 1)
            self.assertEqual(raffi.nama, "raffi")

    def test_add_santri_without_login_redirect_to_login(self):
        resp = self.client.post("/santri/add",
                                data={"nama": "ini nama"})
        self.assert_redirects(resp, "/auth/login?next=%2Fsantri%2Fadd")
        self.assert_message_flashed("You're not logged in", "warning")

        with db_session:
            self.assertEqual(select(s for s in Santri).count(), 6)

    def test_add_santri_logged_user(self):
        self.login()

        resp = self.client.post("/santri/add",
                                data={'nama': 'fukaihah ihfazhillah'})

        self.assert_redirects(resp, "/")
        self.assert_message_flashed("fukaihah ihfazhillah added.", "info")

        with db_session:
            santries = select(s for s in Santri)
            self.assertEqual(santries.count(), 7)
            self.assertIn("fukaihah ihfazhillah", [s.nama for s in santries])

    def test_add_empty_santri_redirect_to_index_page(self):
        self.login()
        resp = self.client.post("/santri/add",
                                data={"nama": ""})
        self.assert_redirects(resp, "/")
        self.assert_message_flashed("Can't add empty santri", "warning")

        with db_session:
            self.assertEqual(select(s for s in Santri).count(), 6)

    def test_anonymous_user_delete_setoran(self):
        resp = self.client.get("/setoran/delete/1")
        self.assert_redirects(resp, "/auth/login?next=%2Fsetoran%2Fdelete%2F1")
        self.assert_message_flashed("You're not logged in", "warning")

    def test_delete_setoran(self):
        self.login()
        resp = self.client.get("/setoran/delete/1")
        self.assert_message_flashed("Setoran with id 1 from santri "
                                    "with id 6 was removed.", "info")
        self.assert_redirects(resp, "/santri/display/6")

        with db_session:
            self.assertEqual(select(s for s in Setoran).count(), 5)

    def test_edit_setoran_without_login(self):
        resp = self.client.post("/setoran/edit/1")
        self.assert_redirects(resp, "/auth/login?next=%2Fsetoran%2Fedit%2F1")
        self.assert_message_flashed("You're not logged in", "warning")

    @db_session
    def test_edit_setoran(self):
        self.login()
        santri = get(s for s in Santri if s.id == 1)
        data = dict(santri='1',
                    start="1/1",
                    end="1/1",
                    jenis="tambah",
                    lulus='1')
        resp = self.client.post("/setoran/edit/1",
                                data=data)
        self.assert_message_flashed("Setoran with id 1 was modified.", "info")
        self.assert_redirects(resp, "/santri/display/1")

        self.assertEqual(select(s for s in Setoran).count(), 6)
        self.assertEqual(santri.setorans.count(), 1)
        enam = get(s for s in Santri if s.id == 6)
        self.assertEqual(enam.setorans.count(), 1)

    @db_session
    def test_add_setoran_anonymous_user_should_redirect_to_login_page(self):
        resp = self.client.post("/setoran/add",
                                data={})
        self.assert_redirects(resp, "/auth/login?next=%2Fsetoran%2Fadd")
        self.assert_message_flashed("You're not logged in", "warning")
