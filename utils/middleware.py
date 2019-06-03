from django.utils.deprecation import MiddlewareMixin


class GetUserOrganization(MiddlewareMixin):

    def process_request(self, request):
        if request.user.id:
            pass

