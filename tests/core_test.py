from datetime import date
from mpbox import create_app
from mpbox.validators import validate_visit
from mpbox.model import Visit, Plan, PlanType
import unittest

class MPBoxTest(unittest.TestCase):

    def test_new_visit(self):
        v = Visit()
        v.date = date(2020, 6, 10)
        p = Plan()
        p.expiry_date = date(2020, 12, 10)

        try:
            validate_visit(v, p)
        except Exception as error:
            self.fail()

        self.assertTrue(True)

    def setUp(self):
        app = create_app().test_client()
        self.response = app.get('/mpbox')
