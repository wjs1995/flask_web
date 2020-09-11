from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from utils import constants

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'accounts_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 用户名,用于登录
    username = db.Column(db.String(64), unique=True, nullable=False)
    # 用户密码
    password = db.Column(db.String(256), nullable=False)
    # 用户昵称
    nickname = db.Column(db.String(64))
    # 用户头像地址
    avatar = db.Column(db.String(256))
    # 用户名是否可以登录
    status = db.Column(
        db.SmallInteger,
        default=constants.UserStatus.USER_ACTIVE.value,
        comment='用户状态')
    # 用户是否为超级管理员
    is_super = db.Column(db.SmallInteger, default=constants.UserRole.COMMON.value)
    # 创建时间
    create_at = db.Column(db.DateTime, default=datetime.now)
    # 修改时间
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 希望在user表通过user.profile取得数据
    # profile = db.relationship('UserProfile')
    """
    id INT NOT NULL AUTO_INCREMENT  COMMENT 'ID' ,
    username VARCHAR(32) NOT NULL   COMMENT '用户名' ,
    password VARCHAR(1024) NOT NULL   COMMENT '密码' ,
    nickname VARCHAR(32) NOT NULL   COMMENT '昵称' ,
    create_at DATETIME    COMMENT '创建时间' ,
    status INT   DEFAULT 1 COMMENT '状态' ,
    is_super INT    COMMENT '是否试管理员' ,
    PRIMARY KEY (id)
    """


class UserProfile(db.Model):
    """用户的详细信息"""
    __tablename__ = 'accounts_user_profile'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 用户名,冗余用户查询
    username = db.Column(db.String(64), unique=True, nullable=False)
    # 关联用户
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 创建时间
    create_at = db.Column(db.DateTime, default=datetime.now)
    # 修改时间
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 希望在user表通过user.profile取得数据
    # 建立用户一对一关系属性
    user = db.relationship('User', backref=db.backref('profile', uselist=False))
    """
      id INT NOT NULL AUTO_INCREMENT  COMMENT 'ID' ,
    user_id INT NOT NULL   COMMENT '关联用户' ,
    username VARCHAR(32)    COMMENT '用户名' ,
    UPDATED_BY VARCHAR(32)    COMMENT '更新人' ,
    UPDATED_TIME DATETIME    COMMENT '更新时间' ,
    PRIMARY KEY (id)
    """
