from django.urls import path
from . import views

urlpatterns = [
    path('', views.endpoints, name="endpoints"),
    path('advocates/', views.advocate_list, name="advocates"),
    path('advocates/search', views.advocate_search),
    path('advocates/<str:username>', views.advocate_info, name='advocate'),
    path('companies/',views.company_list, name="companies"),
    path('companies/<str:name>',views.company_info, name="company") 
]