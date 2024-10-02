from django.urls import path
from . import views

urlpatterns = [
    path('markets/', views.MarketList.as_view(), name='market-list'),
    path('markets/<int:pk>/', views.MarketDetail.as_view(), name='market-detail'),
]