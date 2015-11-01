from flask import Blueprint

main = Blueprint('resources', __name__)

from . import views, errors  # noqa
