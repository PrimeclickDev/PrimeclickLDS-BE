from django.contrib import admin
from .models import Business, Campaign, Lead


class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'leads', 'type_of_campaign', 'converted')
    list_filter = ('type_of_campaign',)


class LeadAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'full_name', 'email', 'phone_number', 'status')
    list_filter = ('campaign', 'campaign', 'status')


admin.site.register(Business, BusinessAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Lead, LeadAdmin)
