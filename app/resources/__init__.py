from flask import Blueprint

resources = Blueprint('resources', __name__)

from . import views, errors  # noqa
