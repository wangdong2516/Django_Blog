from time import sleep

from libs.yuntongxun.CCPRestSDK import REST

# 说明：主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID
_accountSid = '8a216da868747b5801688fc98c6b09c8'

# 说明：主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN
_accountToken = '12ea975a36a64d1dad81b5d1f2c4c49d'

# 请使用管理控制台首页的APPID或自己创建应用的APPID
_appId = '8a216da868747b5801688fc98cc309cf'

# 说明：请求地址，生产环境配置成app.cloopen.com
_serverIP = 'sandboxapp.cloopen.com'

# 说明：请求端口 ，生产环境为8883
_serverPort = '8883'

# 说明：REST API版本号保持不变
_softVersion = '2013-12-26'


# 云通讯官方提供的发送短信代码实例
# # 发送模板短信
# # @param to 手机号码
# # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# # @param $tempId 模板Id
#
# def sendTemplateSMS(to, datas, tempId):
#     # 初始化REST SDK
#     rest = REST(serverIP, serverPort, softVersion)
#     rest.setAccount(accountSid, accountToken)
#     rest.setAppId(appId)
#
#     result = rest.sendTemplateSMS(to, datas, tempId)
#     for k, v in result.iteritems():
#
#         if k == 'templateSMS':
#             for k, s in v.iteritems():
#                 print '%s:%s' % (k, s)
#         else:
#             print '%s:%s' % (k, v)

# 将短信发送的过程使用单利进行封装
# class CCP(object):
#     __instance = None
#
#     # 编写__new__方法
#     def __new__(cls, *args, **kwargs):
#         # 判断该类对象中是否有实例__instance属性
#         if not cls.__instance:
#             cls.__instance = super(CCP, cls).__new__(cls)
#
#             # 初始化REST SDK
#             cls.__instance.rest = REST(_serverIP, _serverPort, _softVersion)
#             cls.__instance.rest.setAccount(_accountSid, _accountToken)
#             cls.__instance.rest.setAppId(_appId)
#
#             return cls.__instance
#         else:
#             return cls.__instance
#
#     def sendTemplateSMS(self, to, datas, tempId):
#
#         result = self.rest.sendTemplateSMS(to, datas, tempId)
#
#         # 只需要告诉自己服务器发送的结果即可,如果返回0表示成功,如果是-1表示失败
#         if result["statusCode"] == "000000":
#             return 0
#         else:
#             return -1


# ccp = CCP()
def send_sms_code(mobile, code_expire_tuple, temp_id):
    # 配置
    rest = REST(_serverIP, _serverPort, _softVersion)
    rest.setAccount(_accountSid, _accountToken)
    rest.setAppId(_appId)
    # 发送
    result = rest.sendTemplateSMS(mobile, code_expire_tuple, temp_id)
    # 结果：信息成功发生，结果字典result中 statuCode 字段为 "000000"
    if result.get("statusCode") == "000000":
        return True  # 表示发送短信成功
    else:
        return False  # 表示发送失败


if __name__ == '__main__':
    # 模板:【云通讯】您使用的是云通讯短信模板，您的验证码是{1}，请于{2}分钟内正确输入
    # 参数解释:
    # 参数1: 表示要发送给那个手机号
    # 参数2: 用来替换模板中的{1},{2}位置的值
    # 参数3: 表示使用的是默认模板

    send_sms_code("18734872516", [666666, 5], 1)
