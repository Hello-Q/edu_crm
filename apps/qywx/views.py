# Create your views here.

from apps.qywx.qywx.callback.WXBizMsgCrypt import WXBizMsgCrypt
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.views import Response
from rest_framework.views import APIView
from apps.qywx.qywx.api.CoreApi import CorpApi, CORP_API_TYPE
from apps.qywx.qywx.api.Conf import *
from apps.qywx.qywx.api.AbstractApi import ApiException
api_app_CUSTOMER_CONTACT = CorpApi(Conf['CORP_ID'], Conf['CUSTOMER_CONTACT'])


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


def request_api(api_app_type, corp_api_type, args=None):
    """对qywx API 发起请求"""
    try:
        response = api_app_type.httpCall(
            corp_api_type, args
        )
        return response

    except ApiException as e:
        response = dict()
        response['errcode'] = e.errCode
        response['e.errmsg'] = e.errMsg
        return response


class FollowUseList(APIView):

    permission_classes = (permissions.IsAuthenticated,)
    @classmethod
    def get_data(cls):
        """请求qywx API 获取跟进人列表"""
        response = request_api(api_app_CUSTOMER_CONTACT, CORP_API_TYPE['GET_FOLLOW_USER_LIST'])
        if response.get('errcode') == 0:
            response['msg'] = '企业共配置{}位员工可添加外部联系人。'.format(len(response['follow_user']))
            return response
        else:
            return response

    def get(self,  request, fromat=None):
        data = self.get_data()
        return Response(data)


class ExternalContactList(APIView):

    permission_classes = (permissions.IsAuthenticated,)
    @classmethod
    def get_data(cls):
        """获取客户列表"""
        follow_user_data = FollowUseList.get_data()
        if follow_user_data['errcode'] != 0:
            return follow_user_data
        else:
            success = 0
            failed = 0
            failed_users = list()
            external_userid = list()
            data = dict()
            for follow_user in follow_user_data['follow_user']:
                response = request_api(api_app_CUSTOMER_CONTACT, CORP_API_TYPE['GET_EXTERNAL_CONTACT_LIST'], {'userid': follow_user})
                print(follow_user)
                if response.get('errcode') == 0:
                    success += 1
                    for external_user in response['external_userid']:
                        external_userid.append(external_user)
                else:
                    failed += 1
                    failed_users.append({'userid': follow_user, 'errcode': response['errcode'], 'checking_url':
                                        'https://open.work.weixin.qq.com/devtool/query?e={0}'.format(response['errcode'])})
            data['errcode'] = 0
            data['errmsg'] = follow_user_data['errmsg'] + '成功为{0}位员工获取了客户, 失败{1}位,拉取客户数{2}位,'.format(success, failed, len(external_userid))
            data['failed_users'] = failed_users
            data['external_userid'] = external_userid
            return data

    def get(self, request, format=None):
        data = self.get_data()
        return Response(data)


class ExternalContactDetail(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get_data(self):
        external_contact_data = ExternalContactList.get_data()
        if external_contact_data['errcode'] != 0:
            return external_contact_data
        success = 0
        external_contact_list = list()
        data = dict()
        for external_contact in external_contact_data['external_userid']:
            response = request_api(api_app_CUSTOMER_CONTACT, CORP_API_TYPE['GET_EXTERNAL_CONTACT_DETAIL'], {'external_userid': external_contact})
            external_contact_list.append(response)
            success += 1
        data['msg'] = external_contact_data['errmsg']
        data['failed_users'] = external_contact_data['failed_users']
        data['external_contact_list'] = external_contact_list
        return data

    def create(self, data):
        for external_contact in data['external_contact_list']:
            pass

    def get(self, request, format=None):
        print(request.user.qywxid)
        data = self.get_data()
        # self.create(data)
        return Response(data)
