from django.urls import path
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'snippets'

urlpatterns = [
	# path('', views.snippet_list),
	# path('snippets/<int:pk>/', views.snippet_detail),
	
	path('', views.SnippetList.as_view(), name='snippet-list'),
	path('<int:pk>/', views.SnippetDetail.as_view(), name='snippet-detail'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
