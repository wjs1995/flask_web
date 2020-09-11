from flask import Flask, session, g
from flask_login import LoginManager
from models import db, User
from flask_ckeditor import CKEditor

from accounts.views import accounts
from qa.views import qa
from utils.filters import number_split

app = Flask(__name__, static_folder='medias')
# 从配置文件加载配置
app.config.from_object('conf.Config')

# 数据库初始化
db.init_app(app)

# ckeditor 初始化
ckeditor = CKEditor()
ckeditor.init_app(app=app)
# 登陆验证
login_manager = LoginManager()
login_manager.login_view = 'accounts.login'
login_manager.login_message = '请登录'
login_manager.login_message_category = 'danger'
login_manager.init_app(app)

# 注册蓝图
app.register_blueprint(accounts, url_prefix='/accounts')
app.register_blueprint(qa, url_prefix='/')

# 注册过滤器
app.jinja_env.filters['number_split'] = number_split


#
# @app.before_request
# def before_request():
#     user_id = session.get('user_id', None)
#     if user_id:
#         user = User.query.get(user_id)
#         print(user)
#         g.current_user = user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
