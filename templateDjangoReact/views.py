from rest_framework.views import APIView
from rest_framework.response import Response

class MyDataView(APIView):
    def get(self, request):
        data = [
            {'id': 1, 'name': 'Item 1'},
            {'id': 2, 'name': 'Item 2'},
            {'id': 3, 'name': 'Item 3'},
        ]
        return Response(data)