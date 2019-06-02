from django.utils.deprecation import MiddlewareMixin


class Row1(MiddlewareMixin):
    def process_request(self,request):
        print('1')
    def process_response(self,request,response):
        print('1')
        return response