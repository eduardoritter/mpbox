from flask import Blueprint

bp = Blueprint("patient", __name__, url_prefix="/patient")


@bp.route("/")
def index():
    return "All Patient"


@bp.route("/create", methods=("GET", "POST"))
def create():
    return "Create Patient"


@bp.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):
    return "Update Patient" + str(id)


@bp.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    return "Delete Patient" + str(id)


@bp.route("/<int:id>/plans", methods=("GET", "POST"))
def plans(id):
    return "Plans" + str(id)


@bp.route("/<int:id>/create_plan", methods=("GET", "POST"))
def create_plan(id):
    return "Create plan" + str(id)