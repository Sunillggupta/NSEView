"""
URL configuration for api app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IndexViewSet, IndexHistoryViewSet, APIStatusViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'indices', IndexViewSet, basename='index')
router.register(r'history', IndexHistoryViewSet, basename='history')
router.register(r'status', APIStatusViewSet, basename='status')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]
