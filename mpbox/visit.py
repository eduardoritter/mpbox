from flask import Blueprint, render_template, request, redirect, request, url_for, flash
from flask_wtf import FlaskForm, Form
from wtforms import SelectField, TextAreaField, BooleanField, DecimalField
from wtforms.validators import DataRequired

from mpbox import db
from mpbox.model import Patient, Plan, Visit, PaymentType, PlanType


bp = Blueprint("visit", __name__, url_prefix="/visit")


@bp.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    return "Delete Visit" + str(id)


@bp.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):
    return "Update Visit"