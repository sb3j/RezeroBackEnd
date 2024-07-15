from django.contrib import admin
from .models import Company

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'business_registration_number', 'phone', 'address', 'detail_address')

admin.site.register(Company, CompanyAdmin)
