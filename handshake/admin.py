from django.contrib import admin
from .models import Employee, Pathway
# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'din',
        'designation',
        'current_company',
        'date_of_appointment',
        'date_of_cessation',
    )
    search_fields = ('user__username', 'din', 'designation')
    list_filter = ('current_company', 'date_of_appointment')


@admin.register(Pathway)
class PathwayAdmin(admin.ModelAdmin):
    list_display = (
        'relationship',
        'target_company',
        'connection_strength',
        'match_score',
        'status',
    )
    search_fields = ('relationship', 'target_company__name')
    list_filter = ('connection_strength', 'status')