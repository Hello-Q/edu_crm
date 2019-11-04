# Create your views here.

from apps.qywx.qywx.callback.WXBizMsgCrypt import WXBizMsgCrypt
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.views import Response, status
from rest_framework.views import APIView
from apps.qywx.qywx.api.CoreApi import CorpApi, CORP_API_TYPE
from apps.qywx.qywx.api.Conf import *
from apps.qywx.qywx.api.AbstractApi import ApiException
from utils.permissions import DataPermission
from apps.clue.models import Clue
from apps.sys.models import User

from apps.clue.serializers import ClueSerializer
import time

# 客户联系应用的secret
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
    """获取微信跟进人列表"""
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


class SyncContacts(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    data_permission = DataPermission

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

    def has_permissions(self, request):
        """
        校验用户权限
        :param request:
        :return:
        """
        perms = ['clue.view_clue', 'clue.add_clue']
        return request.user.has_perms(perms)


    def get_follow_users_qywxid(self, user):
        """
        根据数据权限,返回请求用户个人或部门内人或公司内人qywxid列表
        :param user: 请求用户
        :return: 相关用户列表qywxid列表
        """
        data_perm = self.data_permission().get_data_permission(Clue)
        if data_perm == 10:
            follow_users = User.objects.filter(department__in=user.department.all()).distinct()
        elif data_perm == 30:
            follow_users = User.objects.filter(organization__exact=user.organization)
        else:
            follow_users = [user]
        return follow_users.values('qywxid')

    def get_external_userids(self, user_qywxids):
        """
        :param user_qywxids: 跟进人企业微信id列表
        :return: 外部联系人userid
        """
        external_userids = list()
        for user_qywxid in user_qywxids:
            if user_qywxid['qywxid']:
                response = request_api(api_app_CUSTOMER_CONTACT, CORP_API_TYPE['GET_EXTERNAL_CONTACT_LIST'],
                                       {'userid': user_qywxid['qywxid']})
                if response['errcode'] == 0:
                    external_userids += response['external_userid']

        return external_userids

    def get_external_user_detail(self, external_userids):
        """获取外部联系人详情"""
        for external_userid in external_userids:
            response = request_api(api_app_CUSTOMER_CONTACT, CORP_API_TYPE['GET_EXTERNAL_CONTACT_DETAIL'],
                                   {'external_userid': external_userid})
            yield response

    def processing_data(self, external_user_detail):
        data_list = list()

        for external_user in external_user_detail:
            if external_user['errcode'] == 0:
                """"外部联系人信息"""
                external_contact = external_user['external_contact']

                external_userid = external_contact['external_userid']  # 外部联系人id
                external_name = external_contact['name']
                """跟进人填写信息"""
                follow_user = external_user['follow_user'][0]

                qywxid = follow_user['userid']  # 跟进人企业微信id
                userid = User.objects.get(qywxid=qywxid)

                customer_name = follow_user.get('remark') or external_name  # 客户备注名称
                remark = follow_user['description']  # 客户备注内容
                tel = follow_user['remark_mobiles']  # 客户电话
                channel = follow_user.get('state')  # 添加渠道
                if tel:
                    tel = tel[0]
                create_time = follow_user['createtime']
                create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(create_time))
                external_user_name = external_contact['name']
                data = {
                    'external_userid': external_userid,
                    'channel': channel,
                    'name': customer_name,
                    'tel': tel,
                    'create_time': create_time,
                    'update_time': create_time,
                    'next_time': None,
                    'creator': userid,
                    'operator': userid,
                    'remark': remark,
                }
                data_list.append(data)

        return data_list

    def save_data(self, data_list):
        for data in data_list:
            ser = ClueSerializer(data=data)
            ser.is_valid()
            print(ser.errors)

    def get(self, request, format=None):
        """要求具有线索查看, 新增权限"""
        if not self.has_permissions(request):
            data = {
                'detail': '您没有执行该操作的权限。'
            }
            return Response(data, status=status.HTTP_403_FORBIDDEN)

        follow_users = self.get_follow_users_qywxid(request.user)
        external_userids = self.get_external_userids(follow_users)
        external_user_detail = self.get_external_user_detail(external_userids)
        data = self.processing_data(external_user_detail)
        self.save_data(data)
        return Response({1: 1})
