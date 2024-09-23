from rest_framework import serializers
from .models import HealthRecord, AccessLog

class HealthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthRecord
        fields = ['id', 'patient', 'record_id', 'ipfs_hash', 'created_at']
        read_only_fields = ['patient', 'record_id', 'created_at']

class AccessLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessLog
        fields = ['id', 'record', 'accessed_by', 'access_time', 'transaction_hash']
        read_only_fields = ['accessed_by', 'access_time', 'transaction_hash']