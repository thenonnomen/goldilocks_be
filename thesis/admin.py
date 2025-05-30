from django.contrib import admin

# Register your models here.
from .models import ThesisLibrary, ThesisQueryResult, ThesisCompanyProfile

@admin.register(ThesisQueryResult)
class ThesisQueryResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'query_id', 'created_at')
    search_fields = ('query', 'query_id')
    list_filter = ('created_at',)

@admin.register(ThesisLibrary)
class ThesisLibraryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'finding_summary', 'findings', 'created_at')
    search_fields = ('title', 'description', 'finding_summary')
    list_filter = ('created_at',)

@admin.register(ThesisCompanyProfile)
class ExtendedCompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('company_id', 'country_code', 'founded', 'ceo_name', 'cfo_name')
    search_fields = ('company_id', 'ceo_name', 'cfo_name')
    list_filter = ('country_code', 'founded')