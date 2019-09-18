from flask import Blueprint

bp = Blueprint("plan", __name__, url_prefix="/plan")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):
    return "Update Plan" + str(id)


@bp.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    return "Delete Plan" + str(id)


@bp.route("/<int:id>/visit", methods=("GET", "POST"))
def visit(id):
    return "Plan Visit" + str(id)