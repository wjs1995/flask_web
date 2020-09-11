import hashlib

from flask import request
from flask_login import login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from models import User, db, UserProfile, UserLoginHistory
from utils import constants
from utils.validators import phone_required


class RegisterForm(FlaskForm):
    """用户注册"""
    username = StringField(label='用户名', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入用户名'
    }, validators=[
        DataRequired('请输入用户名'),
        phone_required
    ])
    nickname = StringField(label='用户昵称', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入用户昵称'
    }, validators=[
        DataRequired('请输入用户昵称'),
        Length(min=2, max=20, message='长度在2-20之间')
    ])
    password = PasswordField(label='', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入密码'
    }, validators=[
        DataRequired('请输入密码')
    ])
    confirm_password = PasswordField(label='确认密码', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入确认密码'
    }, validators=[
        DataRequired('请输入确认密码'),
        EqualTo('password', '两次密码输入不一致')
    ])

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('该用户名已经存在')
        return field

    def register(self):
        username = self.username.data
        password = self.password.data
        nickname = self.nickname.data
        try:
            # 将密码加密存储
            password = hashlib.sha256(password.encode()).hexdigest()
            user_obj = User(username=username, password=password, nickname=nickname)
            db.session.add(user_obj)
            profile = UserProfile(username=username, user=user_obj)
            db.session.add(profile)
            db.session.commit()
            return user_obj
        except Exception as e:

            return None


class LoginForm(FlaskForm):
    username = StringField(label='用户名', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入用户名'
    }, validators=[
        DataRequired('请输入用户名'),
        phone_required
    ])
    password = PasswordField(label='', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入密码'
    }, validators=[
        DataRequired('请输入密码')
    ])

    def validate(self):
        result = super().validate()
        username = self.username.data
        password = self.password.data
        password = hashlib.sha256(password.encode()).hexdigest()
        if result:
            user = User.query.filter_by(username=username, password=password).first()
            if user is None:
                result = False
                self.username.errors = ['用户名或密码错误']
            elif user.status == constants.UserStatus.USER_IN_ACTIVE.value:
                result = False
                self.username.errors = ['用户已被禁用']
        return result

    """执行登录的逻辑代码"""

    def do_login(self):
        username = self.username.data
        password = self.password.data
        password = hashlib.sha256(password.encode()).hexdigest()
        try:
            # TODO 验证加密后的密码是否正确
            # 1 查找用户
            user = User.query.filter_by(username=username, password=password).first()
            print('user:', user)
            # 2 登录用户
            # session['user_id'] = user.id
            # TODO 用flask-login代替
            login_user(user)
            # 3 记录日志
            ip = request.remote_addr
            ua = request.headers.get('user-agent', None)
            obj = UserLoginHistory(username=username, ip=ip, ua=ua, user=user)
            db.session.add(obj)
            db.session.commit()
        except Exception as e:
            print(e)
            return None
        return user
