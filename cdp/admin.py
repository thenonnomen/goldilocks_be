from django.contrib import admin
from cdp.models import GoldilocksCDP, PrimaryCompanyInfo, SecondaryCompanyInfo, BusinessTracker, FinancialInfo
# Register your models here.


class GoldilocksGDPAdmin(admin.ModelAdmin):
    list_display = ['name', 'headquarters', 'sector', 'industry', 'ceo', 'cfo']
admin.site.register(GoldilocksCDP, GoldilocksGDPAdmin)

admin.site.register(PrimaryCompanyInfo)
admin.site.register(SecondaryCompanyInfo)
admin.site.register(BusinessTracker)
admin.site.register(FinancialInfo)