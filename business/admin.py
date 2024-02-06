from django.contrib import admin
from .models import Business, CallReport, Campaign, Lead, FormDesign


class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'leads',
                    'type_of', 'created', 'converted', 'call_scenario_id')
    list_filter = ('type_of',)


class LeadAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'full_name', 'email',
                    'phone_number', 'created', 'status')
    list_filter = ('campaign', 'campaign', 'status')


class FormDesignAdmin(admin.ModelAdmin):
    list_display = ('design',)


admin.site.register(FormDesign, FormDesignAdmin)
admin.site.register(CallReport)
admin.site.register(Business, BusinessAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Lead, LeadAdmin)
