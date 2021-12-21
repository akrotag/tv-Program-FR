from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "s56e2c89re6t1K27e3y568"

    from .views import views
    from .now import now_bp

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(now_bp, url_prefix='/')

    return app