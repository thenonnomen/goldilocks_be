from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ThesisLibraryViewSet, ThesisQueryResultViewSet, ThesisCompanyProfileViewSet, ExcelUploadView

router = DefaultRouter()
router.register(r'library', ThesisLibraryViewSet, basename='thesislibrary')
router.register(r'queries', ThesisQueryResultViewSet, basename='thesisqueryresult')
router.register(r'companies', ThesisCompanyProfileViewSet, basename='company')

urlpatterns = [
    path('', include(router.urls)),
    path('upload-companies/', ExcelUploadView.as_view(), name='upload-companies'),
]
