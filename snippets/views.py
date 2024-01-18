from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from django.http import Http404, HttpResponseNotAllowed, JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.views import APIView
from rest_framework import status

"""test_data = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'title': openapi.Schema(type=openapi.TYPE_STRING, description='Enter your title here'),
        'code': openapi.Schema(type=openapi.TYPE_STRING, description='Enter your code here'),
        'linenos': openapi.Schema(type=openapi.TYPE_BOOLEAN, default=True),
        'language': openapi.Schema(type=openapi.TYPE_STRING, description='Enter the language of the code'),
        'style': openapi.Schema(type=openapi.TYPE_STRING, description='Enter the style of the code'),
    }
)


# Create your views here.
# Function based views
@swagger_auto_schema(method='get', responses={200: SnippetSerializer(many=True)}, operation_summary='Get All Snippets')
@swagger_auto_schema(method='post', request_body=test_data, responses={201: SnippetSerializer()}, operation_summary='Create a Snippet')
@api_view(['GET', 'POST'])  # decorator to expose the function to the web
def snippet_list(request, format=None):
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = request.data
        # data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


@swagger_auto_schema(method='get', responses={200: SnippetSerializer()}, operation_summary='Get Snippet by ID')
@swagger_auto_schema(method='patch', request_body=test_data, responses={200: SnippetSerializer()}, operation_summary='Update Snippet')
@swagger_auto_schema(method='delete', responses={204: ''}, operation_summary='Delete Snippet')
@api_view(['GET', 'PATCH', 'DELETE'])
def snippet_detail(request, pk, format=None):
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PATCH':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=404)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
"""

# Class Based Views
# class SnippetList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     @swagger_auto_schema(responses={200: SnippetSerializer(many=True)}, operation_summary='Get All Snippets')
#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()
#         serializer= SnippetSerializer(snippets, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     @swagger_auto_schema(request_body=SnippetSerializer, responses={201: SnippetSerializer()}, operation_summary='Create a Snippet')
#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)


# class SnippetDetail(APIView):
#     """
#     Retieve, update or delete a snippet instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404

#     @swagger_auto_schema(responses={200: SnippetSerializer()}, operation_summary='Get Snippet by ID')
#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return JsonResponse(serializer.data, safe=False)

#     @swagger_auto_schema(request_body=SnippetSerializer, responses={200: SnippetSerializer()}, operation_summary='Update Snippet')
#     def patch(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, safe=False)
#         return JsonResponse(serializer.errors, status=status.HTTP_404_NOT_FOUND, safe=False)

#     @swagger_auto_schema(responses={204: ''}, operation_summary='Delete Snippet')
#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return HttpResponse(status=status.HTTP_204_NO_CONTENT)


# Using mixins
from rest_framework import mixins
from rest_framework import generics


class SnippetList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    @swagger_auto_schema(responses={200: SnippetSerializer(many=True)}, operation_summary='Get All Snippets')
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(request_body=SnippetSerializer, responses={201: SnippetSerializer()}, operation_summary='Create a Snippet')
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SnippetDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    @swagger_auto_schema(responses={200: SnippetSerializer()}, operation_summary='Get Snippet by ID')
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(request_body=SnippetSerializer, responses={200: SnippetSerializer()}, operation_summary='Update Snippet')
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(responses={204: ''}, operation_summary='Delete Snippet')
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
