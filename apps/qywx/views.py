from django.shortcuts import render
# Create your views here.

from .callback.WXBizMsgCrypt import WXBizMsgCrypt
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.views import APIView


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
        # print(data)
        return HttpResponse(data)


base_url = 'https://qyapi.weixin.qq.com/'


class UpdateExternalUser(APIView):

    def get(self, request, format=None):
        pass