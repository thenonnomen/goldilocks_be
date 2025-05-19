from django.contrib import admin
from cdp.models import GoldilocksCDP, PrimaryCompanyInfo, SecondaryCompanyInfo, BusinessTracker, FinancialInfo, UserSearchPrompts
# Register your models here.


class GoldilocksGDPAdmin(admin.ModelAdmin):
    list_display = ['name', 'headquarters', 'sector', 'industry', 'ceo', 'cfo']
admin.site.register(GoldilocksCDP, GoldilocksGDPAdmin)

class UserPromptAdmin(admin.ModelAdmin):
    list_display = ['user', 'prompt', 'timestamp']
admin.site.register(UserSearchPrompts, UserPromptAdmin)

class FinancialInfoAdmin(admin.ModelAdmin):
    list_display = ['primary_info', 'revenue', 'employee_count', 'first_name_ceo']
admin.site.register(FinancialInfo, FinancialInfoAdmin)

class BusinessTrackerAdmin(admin.ModelAdmin):
    list_display = ['primary_info', 'total_visits', 'organic_social_visits']
admin.site.register(BusinessTracker, BusinessTrackerAdmin)

class SecondaryCompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['primary_info', 'employee_count', 'investors']
admin.site.register(SecondaryCompanyInfo, SecondaryCompanyInfoAdmin)

class PrimaryCompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'company_domain', 'founded', 'company_size']
admin.site.register(PrimaryCompanyInfo, PrimaryCompanyInfoAdmin)