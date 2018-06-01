
from flask import Flask

from authentification.order_views import order_blueprint
from ihome_utils.setting import TEMPLATES_DIR, STATIC_DIR
from authentification.views import user
from authentification.house_views import house_blueprint
from ihome_utils.functions import init_ext


def create_app(config):
    """defind app
    """
    app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

    app.config.from_object(config)
    app.register_blueprint(blueprint=user, url_prefix='/user')
    app.register_blueprint(blueprint=house_blueprint, url_prefix='/house')
    app.register_blueprint(blueprint=order_blueprint, url_prefix='/order')

    init_ext(app)

    return app