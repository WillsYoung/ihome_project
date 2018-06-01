
import redis
from ihome_utils.setting import SQLALCHEY_DATABASE_URI


class Config():

    # 配置 mysql数据库
    SQLALCHEMY_DATABASE_URI = SQLALCHEY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 配置 redis数据库
    SECRET_KET = 'secret_key'
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.Redis(
        host='47.106.162.144',
        password='yqx123456',
    )
    SESSION_KEY_PREFIX = 'iHome_user'

