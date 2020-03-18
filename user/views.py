from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.


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