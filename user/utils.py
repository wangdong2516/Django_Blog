"""
    用户相关的工具
"""
import re

from django.contrib.auth.backends import ModelBackend

from .models import User


class UsereAuthBackend(ModelBackend):
    """
        用户认证后端类
        验证用户是否存在以及密码是否正确
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
            重写父类的认证方法，添加自定义的逻辑
        :param request:
        :param username: 用户名
        :param password: 密码
        :param kwargs:
        :return:
        """
        try:
            # 支持手机号作为用户名
            if re.match(r'1[3-9\d{9}$]', username):
                user = User.objects.get(mobile=username)
            else:
                user = User.objects.get(username=username)
        except:  # noqa E722
            # 如果当前用户不存在，将用户对象设置为None值
            user = None

        if user is not None and user.check_password(password):
            return user
        else:
            return user
