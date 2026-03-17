from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def add(x, y):
    logger.info(f'Adding {x} + {y}')
    return x + y

@shared_task
def multiply(x, y):
    logger.info(f'Multiplying {x} * {y}')
    return x * y
