# myapp/tasks.py
from celery import shared_task

from AIT.ait import make_voice_call
from business.models import Lead

@shared_task(bind=True, max_retries=3, soft_time_limit=300)
def process_call_batch(self, batch_nums, campaign_id):
    try:
        make_voice_call(batch_nums, campaign_id)
    except Exception as exc:
        # Retry the task if it fails
        raise self.retry(exc=exc, countdown=60)

@shared_task(bind=True)
def launch_calls(self, nums, campaign_id):
    batch_size = 20
    for i in range(0, len(nums), batch_size):
        batch_nums = nums[i:i + batch_size]
        process_call_batch.delay(batch_nums, campaign_id)
