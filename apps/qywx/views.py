# Create your views here.

from apps.qywx.qywx.callback.WXBizMsgCrypt import WXBizMsgCrypt
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.views import Response
from rest_framework.views import APIView
from apps.qywx.qywx.api.CoreApi import CorpApi, CORP_API_TYPE
from apps.qywx.qywx.api.Conf import *
from apps.qywx.qywx.api.AbstractApi import ApiException
api = CorpApi(Conf['CORP_ID'], Conf['CUSTOMER_CONTACT'])


class CallbackService(APIView):
    """微信回调服务"""
    permission_classes = (permissions.AllowAny,)
    sToken = 'spsus4qozlVK17M'
    sEncodingAESKey = 'wHANXiWXSnlnFcGVlCATYAI2ochnVV1dQHWXmlkLbyP'
    sReceiveId = 'wwca091e6a98bdcfb7'
    msg_crypt = WXBizMsgCrypt(sToken=sToken, sEncodingAESKey=sEncodingAESKey, sReceiveId=sReceiveId)

    def get(self, request, format=None):
        msg_signature = request.GET.get('msg_signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        echostr = request.GET.get('echostr')
        data = self.msg_crypt.VerifyURL(msg_signature, timestamp, nonce, echostr)[1]
        return HttpResponse(data)

    def post(self, request, format=None):
        msg_signature = request.GET.get('msg_signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        echostr = request.body
        data = self.msg_crypt.DecryptMsg(echostr, msg_signature, timestamp, nonce)
        print(data[1].decode())
        return HttpResponse(data)


base_url = 'https://qyapi.weixin.qq.com/'


class GetFollowUseList(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, fromat=None):
        try:
            ##
            response = api.httpCall(
                CORP_API_TYPE['GET_FOLLOW_USER_LIST'],
                )
            print(response)
        except ApiException as e :
            response = (e.errCode, e.errMsg)

            ##


        return Response(response['follow_user'])