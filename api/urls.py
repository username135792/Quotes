from django.urls import path
from . import views

urlpatterns = [
    path('', views.Quote_list, name='index'),
    path('quotes/', views.Quote_list_create, name='quote_list_create'),
    path('quotes/<int:quote_id>/', views.Quote_detail_delete_update, name='quote_detail_delete_update'),
    path('tags/', views.tag_list_create, name='tag_list'),
    path('tags/<int:tag_id>/', views.tag_detail_delete_update, name='tag_detail_delete_update'),
    path('tags/<int:tag_id>/quotes/', views.Quote_via_tag_id, name='quote_via_tag_id'),
    path('quotes/random', views.quote_random, name='quote_random'),
]