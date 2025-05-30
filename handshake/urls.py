from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, PathwayViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'pathways', PathwayViewSet, basename='pathway')

urlpatterns = [
    path('', include(router.urls)),
]
