import os


class Config(object):
    # 数据配置URI
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1:3306/flask_qa'
    # flash, form, wtf
    SECRET_KEY = '123abc321'
    # 文件上传根路径
    MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'medias')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
