from celery import shared_task
from celery.utils.log import get_task_logger

from .utils import create_new_story

logger = get_task_logger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 5},
)
def new_story(self):
    logger.info("Created a new story.")
    create_new_story()
