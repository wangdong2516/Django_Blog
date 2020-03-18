import random
from datetime import datetime

from django.shortcuts import render
from django_redis import get_redis_connection

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView

from .models import User
from user.serializers import UserRegisterSerializer, MyTokenObtainPairSerializer
from libs.yuntongxun.send_sms import send_sms_code


class IndexView(APIView):
	"""
		首页视图(登录页视图)
	"""

	def get(self, request) -> render:
		"""
			获取博客首页
		:param request: DRF封装的请求对象
		:return: 首页模板
		"""
		return render(request, 'login.html')


class MobileVerifyView(APIView):
	"""
		手机号校验视图
	"""
	def get(self, request, mobile: str) -> Response:
		"""
			注册时校验该手机号对应的用户是否存在，返回count
		:param request: 请求对象
		:param mobile: 手机号
		:return: 0 or 1(int)
		"""
		count = User.objects.filter(mobile=mobile).count()

		return Response({'count': count})


class UserNameVerifyView(APIView):
	"""
		用户名校验视图
	"""

	def get(self, request, username: str) -> Response:
		"""
			注册时校验该用户名是否已经存在，返回count
		:param username: 用户名
		:return: 0 or 1(int)
		"""
		count = User.objects.filter(username=username).count()
		return Response({'count': count})


class SmsCodeView(APIView):
	"""
		发送短信验证码的视图
		采用的是6位短信验证码，基于redis进行存储
	"""

	def get(self, request):
		"""
			获取短信验证码,一分钟之内不能重复发送短信验证码，短信验证码5分钟之内有效
			重新发送的短信验证码会将原来的短信验证码覆盖
		:param request: 请求对象
		:return: sms_code
		"""
		mobile = request.query_params.get('mobile')
		sms_code = random.randint(100000, 999999)
		conn = get_redis_connection('default')
		# 首先获取缓存中的短信验证码标志位
		sms_code_flag = f'sms_code_flag_{mobile}'
		flag = conn.get(sms_code_flag)
		print(sms_code)
		if flag:
			return Response({'error': '短信验证码发送过于频繁，请一分钟之后再试'})
		redis_key = f'sms_code_{mobile}'
		conn.set(redis_key, str(sms_code), 300)
		conn.set(sms_code_flag, str(sms_code), 60)
		send_sms_code(mobile, [str(sms_code), '5'], 1)
		return Response({'message': 'ok'})


class UserRegisterView(CreateAPIView):
	"""
		用户注册视图，使用CreateAPIView实现
	"""
	serializer_class = UserRegisterSerializer


class LoginView(TokenObtainPairView):

	"""
		用户登录视图
	"""
	serializer_class = MyTokenObtainPairSerializer

	def post(self, request, *args, **kwargs):
		"""
			用户登录(V.01)只支持当前网页登录，后面会扩展为支持第三方登录
			使用jwt进行状态保持
			重写父类的方法，登录之前验证当前用户的有效性
		:param request: 请求对象
		:return:
		"""
		# 调用父类的post方法生成响应对象
		response = super().post(request, *args, **kwargs)
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():
			# 从MyTokenObtainPairSerializer序列化器中获取验证后的用户对象
			user = serializer.validated_data.get('user') or request.user
			# 获取验证后的数据并且将最后登录时间置为当前时间
			user.last_login = datetime.now()
			user.save()
			response.data.pop('user')
			return response
		return response







