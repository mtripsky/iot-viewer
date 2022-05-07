from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = 'jsfdnsdaeud'

    from . import viewer
    app.register_blueprint(viewer.bp)

    return app
