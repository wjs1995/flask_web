"""常量的配置"""
from enum import Enum


class UserStatus(Enum):
    """用户状态"""
    # 启用，可以登录
    USER_ACTIVE = 1
    # 禁用，不能登录
    USER_IN_ACTIVE = 0


class UserRole(Enum):
    # 普通用户使用前台功能
    COMMON = 0
    # 管理员，使用后台管理
    ADMIN = 1
    # 超级管理员，删除敏感数据
    SUPER_ADMIN = 2
