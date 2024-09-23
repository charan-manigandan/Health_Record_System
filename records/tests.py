from django.test import TestCase
from django.contrib.auth.models import User
from .models import HealthRecord
from .blockchain import create_record, grant_access, revoke_access, get_record

class HealthRecordTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.record = HealthRecord.objects.create(
            patient=self.user,
            ipfs_hash='QmXnnyufdzAWL5CqZ2RnSNgPbvCc1ALT73s6epPrRnZ1Xy'
        )

    def test_health_record_creation(self):
        self.assertEqual(HealthRecord.objects.count(), 1)
        self.assertEqual(self.record.patient, self.user)