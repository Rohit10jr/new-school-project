from rest_framework import pagination
from rest_framework.response import Response
from django.http import JsonResponse

class Pagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })
    
def response_for_404(request, exception=None):
    return JsonResponse({'status_code': '404', 'details': 'error'}, status=404)