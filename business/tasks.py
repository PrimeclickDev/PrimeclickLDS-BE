# business/tasks.py
from celery import shared_task
from AIT.ait import make_voice_call


@shared_task
def process_voice_calls(nums, campaign_id):
    make_voice_call(nums, campaign_id)
