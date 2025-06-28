import os.path


class Config(object):
    APPNAME = 'app'
    ROOT = os.path.abspath(APPNAME)
    UPLOAD_PATH = '/static/upload/'
    SERVER_PATH = ROOT + UPLOAD_PATH

    SQLALCHEMY_DATABASE_URI = "sqlite:///shop.db"
    SECRET_KEY = "jfkhdlkshlj54hl65hkejdlkjfhsaiuugd78fsdhiuhifs32"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
