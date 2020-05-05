from datetime import date
from mpbox import create_app
from mpbox.validators import validate_visit, ValidationError
from mpbox.model import Visit, Plan, PlanType
import unittest

class MPBoxTest(unittest.TestCase):

    def test_visit_date(self):
        v = Visit(date=date(2020, 4, 10))
        v.plan = Plan(expiry_date=date(2020, 12, 10))

        try:
            validate_visit(v)
        except Exception:
            self.fail()
        
        pass

    def test_visit_expired_plan(self):
        v = Visit(date=date(2020, 4, 4))
        v.plan = Plan(expiry_date = date(2020, 4, 1))

        with self.assertRaises(ValidationError):
            validate_visit(v)


    def setUp(self):
        app = create_app().test_client()
        self.response = app.get('/mpbox')
