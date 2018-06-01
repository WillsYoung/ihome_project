
from flask_script import Manager

from ihome_utils import create_app
from ihome_utils.config import Config


app = create_app(Config)
manage = Manager(app)


if __name__ == '__main__':
    manage.run()
