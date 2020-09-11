import hashlib

from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user

from accounts.forms import RegisterForm, LoginForm
from models import User, UserLoginHistory, db

accounts = Blueprint('accounts', __name__,
                     template_folder='templates',
                     static_folder='../assets')


@accounts.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    next_url = request.values.get('next', url_for('qa.index'))
    if form.validate_on_submit():
        user = form.do_login()
        if user:
            # 4 跳转到首页
            flash('{}欢迎回来'.format(user.nickname), 'success')
            return redirect(next_url)
        else:
            flash('登陆失败', 'danger')


    # else:
    #     print(form.errors)
    #     print(form.username.data)
    #     print(form.password.data)
    return render_template('login.html', form=form, next_url=next_url)


@accounts.route('logout')
def logout():
    logout_user()
    flash('退出成功', 'success')
    return redirect(url_for('accounts.login'))


@accounts.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_obj = form.register()
        if user_obj:
            flash('注册成功', 'success')
            return redirect(url_for('accounts.login'))
        else:
            flash('注册失败', 'danger')
    print(form.username.errors)
    return render_template('register.html', form=form)


@accounts.route('/mine')
def mine():
    return render_template('mine.html')
