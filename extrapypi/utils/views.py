"""Utils views
"""
from flask import Blueprint, render_template

blueprint = Blueprint('utils', __name__)


@blueprint.route('/ping', methods=['GET'])
def ping():
    """Simple view used to monitor extrapypi server"""
    return "pong", 200


@blueprint.route('/', methods=['GET'])
def home():
    """Simple view used to monitor extrapypi server"""
    return render_template('index.html')


@blueprint.errorhandler(404)
def page_not_found(e):
    return render_template('utils/404.html'), 404


@blueprint.errorhandler(500)
def internal_server_error(e):
    return render_template('utils/500.html'), 500  # pragma: no cover
