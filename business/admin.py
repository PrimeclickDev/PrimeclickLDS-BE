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
                    'phone_number', 'created', 'status', 'contacted_status')
    list_filter = ('campaign', 'campaign', 'status')


class CallReportAdmin(admin.ModelAdmin):
    list_display = ('sent_at', 'campaign', 'lead', 'to_number',)

    list_filter = ('campaign',)


class FormDesignAdmin(admin.ModelAdmin):
    list_display = ('id', 'design',)


admin.site.register(FormDesign, FormDesignAdmin)
admin.site.register(CallReport, CallReportAdmin)
admin.site.register(Business, BusinessAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Lead, LeadAdmin)
