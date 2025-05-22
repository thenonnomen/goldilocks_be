from rest_framework import routers
from .views import (
                    GoldilocksCDPViewSet, PrimaryCompanyInfoViewSet,
                    SecondaryCompanyInfoViewSet, FinancialInfoViewSet, 
                    BusinessTrackerViewSet
                    )
from django.urls import include, path

router = routers.DefaultRouter()

router.register(r'goldilocks', GoldilocksCDPViewSet)
router.register(r'primary_company_info', PrimaryCompanyInfoViewSet)
router.register(r'sec_company_info', SecondaryCompanyInfoViewSet)
router.register(r'financial_info', FinancialInfoViewSet)
router.register(r'business_tracker', BusinessTrackerViewSet)

urlpatterns = []

urlpatterns = router.urls