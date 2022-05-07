from flask import (
    render_template,
    Blueprint,
)

bp = Blueprint("viewer", __name__)


@bp.route("/")
def home():
    return render_template("home.html")


@bp.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404
