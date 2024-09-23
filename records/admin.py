from django.contrib import admin
from .models import HealthRecord, AccessLog

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'record_id', 'created_at']
    search_fields = ['patient__username', 'record_id']

@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ['record', 'accessed_by', 'access_time', 'transaction_hash']
    list_filter = ['access_time']