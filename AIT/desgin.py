import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField


class AccessTime(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_access_time = models.DateTimeField()
    end_access_time = models.DateTimeField()



class AccessTimeConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module = models.CharField(max_length=100)
    weekdays_access_time = models.ForeignKey(AccessTime, on_delete=models.CASCADE, related_name="weekdays_access_time")
    weekends_access_time = models.ForeignKey(AccessTime, on_delete=models.CASCADE, related_name="weekends_access_time")
    holidays_access_time = models.ForeignKey(AccessTime, on_delete=models.CASCADE, related_name="holidays_access_time")
    global_access_time = models.ForeignKey(AccessTime, on_delete=models.CASCADE, related_name="global_access_time")
    exempted_user = ArrayField(models.CharField(max_length=100), blank=True)
    exempted_branches = ArrayField(models.CharField(max_length=100), blank=True)


class GlobalAccessTime(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_access_time = models.DateTimeField()
    end_access_time = models.DateTimeField()