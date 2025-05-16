from django.contrib import admin
from cdp.models import GoldilocksCDP
# Register your models here.


class GoldilocksGDPAdmin(admin.ModelAdmin):
    list_display = ['name', 'headquarters', 'sector', 'industry', 'ceo', 'cfo']
admin.site.register(GoldilocksCDP, GoldilocksGDPAdmin)