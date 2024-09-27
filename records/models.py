from django.db import models
from django.contrib.auth.models import User
from web3 import Web3

class HealthRecord(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_records')
    doctor = models.ManyToManyField(User, related_name='doctor', blank=True)
    record_name = models.CharField(max_length=50, null=True, blank=True)
    record_id = models.CharField(max_length=66, unique=True)
    ipfs_hash = models.CharField(max_length=46)
    signature = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.record_id:
            self.record_id = Web3.keccak(text=f"{self.patient.id}:{self.ipfs_hash}").hex()
        super().save(*args, **kwargs)

class AccessLog(models.Model):
    record = models.ForeignKey(HealthRecord, on_delete=models.CASCADE, related_name='access_logs')
    accessed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    access_time = models.DateTimeField(auto_now_add=True)
    transaction_hash = models.CharField(max_length=66)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public_key = models.TextField()

    def __str__(self):
        return self.user.username