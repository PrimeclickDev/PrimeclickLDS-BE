from django.contrib import admin
from .models import Business, CallReport, Campaign, Lead, FormDesign, ViewTimeHistory, ActivityLog


class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'leads',
                    'type_of', 'created', 'converted')
    list_filter = ('type_of',)


class LeadAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'full_name', 'email',
                    'phone_number', 'created', 'status', 'contacted_status')
    list_filter = ('campaign', 'campaign', 'status')


class CallReportAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'lead', 'report')

    list_filter = ('campaign',)


class FormDesignAdmin(admin.ModelAdmin):
    list_display = ('id', 'design',)


admin.site.register(FormDesign, FormDesignAdmin)
admin.site.register(CallReport, CallReportAdmin)
admin.site.register(Business, BusinessAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Lead, LeadAdmin)
admin.site.register(ViewTimeHistory)
admin.site.register(ActivityLog)