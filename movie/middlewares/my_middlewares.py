# -*- coding = utf-8 -*-
# @Time : 2020/12/13 18:52
# @Author : Chenih
# @File : my_middlewares.py
# @Software : PyCharm
import re

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class AuthMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        # 需要登陆后访问的地址要验证登陆状态

        # 拿到请求的路径，然后与列表中的路径作对比
        # 默认所有路径都需要验证，如果请求的路径在列表中，那么就不用验证就可以进入
        url = request.path_info
        for i in [r'^/user/login/$', r'^/user/userreg/$']:
            if re.match(i, url):
                # 请求的路径是列表中的路径那么直接返回，不再阻拦
                return

        # 校验登录状态
        is_login = request.session.get('is_login')
        if is_login:
            # 已经登陆，可以访问，直接return
            return
        else:
            # 未登录，跳转到登陆页面
            return redirect('/user/login')

