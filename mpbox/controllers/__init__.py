from . import auth, home, patient, plan, visit, dashboard, finance

default_blueprints = [
    auth.bp,
    home.bp,
    patient.bp,
    plan.bp,
    visit.bp,
    dashboard.bp,
    finance.bp,
]
