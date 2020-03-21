"""
    与用户相关的序列化器在这里定义
"""
import re
from datetime import datetime

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from django_redis import get_redis_connection

from user.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """
        用户注册的序列化器,是根据模型类生成的序列化器
    """
    sms_code = serializers.CharField(
        min_length=6, max_length=6, write_only=True)
    allow = serializers.BooleanField(write_only=True)
    confirm_password = serializers.CharField(
        min_length=6, max_length=16, write_only=True)
    token = serializers.CharField(label='token', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'mobile', 'sms_code',
            'allow', 'confirm_password', 'token'
        ]
        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20位的用户名长度',
                    'max_length': '仅允许5-20位的用户名长度',
                }
            },
            'password': {
                'min_length': 6,
                'max_length': 20,
                'write_only': True,
                'error_messages': {
                    'min_length': '仅允许6-20位密码长度',
                    'max_length': '仅允许6-20位密码长度',
                }
            }
        }

    def validate_mobile(self, attrs):
        """
            验证用户手机号，单一字段的验证方法
        :param attrs: 需要验证的手机号
        :return: attrs 经过验证后的数据
        """
        if not re.match(r'^1[3-9]\d{9}$', attrs):
            raise serializers.ValidationError('手机号格式错误')
        return attrs

    def validate(self, attrs):
        """
            多个字段的验证方法
        :param attrs: 需要验证的数据，序列化器类中定义的字段
        :return:
        """

        # 协议的验证
        allow = attrs.get('allow')
        if allow is not True:
            raise serializers.ValidationError('请勾选同意用户协议')

        # 两次输入密码一致性的验证
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password and any([password, confirm_password]):
            raise serializers.ValidationError('两次密码输入不一致，请重新输入')

        # 短信验证码的验证
        sms_code = attrs.get('sms_code')
        conn = get_redis_connection('default')
        redis_key = 'sms_code_{}'.format(attrs.get('mobile'))
        # 这里直接从redis获取到的短信验证码是字节类型的，需要解码
        real_sms_code = conn.get(redis_key).decode()
        if not real_sms_code:
            raise serializers.ValidationError('短信验证码已无效，请点击重新发送')
        if sms_code != real_sms_code:
            raise serializers.ValidationError('短信验证码输入错误，请重新输入')
        return attrs

    def create(self, validated_data: dict):
        """
            重写序列化器的create方法，实现我们自己的保存用户的逻辑
            主要做的有以下几件事：
                1. 删除验证数据中的sms_code字段，不需要保存到数据库中
                2. 删除验证数据中的conifrm_password字段，不保存到数据库中
                3. 删除验证数据中的allow字段，不保存到数据库中
                4. 发布token，实现基于JWT的状态保持
                5. 设置用户的登录时间
        :param validated_data: 验证后的数据
        :return: user用户对象
        """
        validated_data.pop('sms_code')
        validated_data.pop('confirm_password')
        validated_data.pop('allow')

        # 保存当前用户,create_user可以快速保存一个用户对象
        # 原因是在执行迁移的时候，django将User模型类的objects管理器
        # 重新复制为('objects', django.contrib.auth.models.UserManager())的实例
        # UserManager中有这个方法
        user = User.objects.create_user(**validated_data)
        refresh = RefreshToken.for_user(user)
        # 将token进行返回
        user.token = refresh
        user.last_login = datetime.now()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):  # noqa E501
    """
        定义自己的token验证序列化器
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        # 返回当前登录的用户对象
        data['user'] = self.user
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data
