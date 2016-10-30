from flask_testing import TestCase
from create_app import create_app
from webmodules.setoran.forms import SetoranForm


class CustomValidatorTestCase(TestCase):

    def setUp(self):
        self.setoran_form = SetoranForm()

    def create_app(self):
        app = create_app("flask_config.Testing")
        return app

    def test_start_end_cant_filled_with_non_numeric(self):
        self.setoran_form.start.data = "lklsjalfdj"
        self.setoran_form.end.data = "klsjflajf"

        self.assertFalse(self.setoran_form.start.validate(self.setoran_form))
        self.assertFalse(self.setoran_form.end.validate(self.setoran_form))