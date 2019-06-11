from django.utils.deprecation import MiddlewareMixin


class GetUserOrganization(MiddlewareMixin):

    def process_request(self, request):
        print(request)

