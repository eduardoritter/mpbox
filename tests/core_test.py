from datetime import date
from mpbox import create_app
from mpbox.validators import validate_visit
from mpbox.model import Visit, Plan, PlanType
import unittest

class MPBoxTest(unittest.TestCase):

    def test_visit_date(self):
        v = Visit(date=date(2020, 6, 10))
        p = Plan(expiry_date=date(2020, 12, 10))

        try:
            validate_visit(v, p)
        except Exception:
            self.fail()
        
        pass

    def test_visit_expired_plan(self):
        v = Visit(date=date(2020, 12, 11))
        p = Plan(expiry_date = date(2020, 12, 10))

        with self.assertRaises(Exception):
            validate_visit(v, p)


    def setUp(self):
        app = create_app().test_client()
        self.response = app.get('/mpbox')
