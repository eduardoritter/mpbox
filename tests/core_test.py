from datetime import date
from mpbox.utils import validate_visit,  ValidationError
from mpbox.models import Visit, Plan
import unittest

class MPBoxTest(unittest.TestCase):


    def test_two_visits_on_same_day(self):

        plan = Plan(expiry_date=date(2020, 12, 10))
        plan.visits.append(Visit(date=date(2020, 4, 10)))
        
        v = Visit(date=date(2020, 4, 10))

        # with self.assertRaises(ValidationError):
        #     validate_new_visit(v, plan)


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


