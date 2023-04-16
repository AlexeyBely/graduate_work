import asyncio
import logging
from asgiref.sync import async_to_sync
from celery import Celery
from celery.schedules import crontab

from core.config import settings
from billing.billing_offer import get_billing_offer
from db import psql_async


logger = logging.getLogger('')


url_broker = 'amqp://{0}:{1}@{2}:{3}/{4}'.format(
    settings.rabbitmq_default_user,
    settings.rabbitmq_default_pass,
    settings.billing_rabbitmq_host,
    settings.billing_rabbitmq_port,
    settings.rabbitmq_default_vhost,
)

app = Celery('billing', broker=url_broker)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Check payments and refunds in payment system.
    sender.add_periodic_task(15.0, 
                             load_payment_system.s(), 
                             name='load from payment system')


@app.task
def load_payment_system():
    billing = get_billing_offer()
    async_to_sync(billing.check_payments)()
    async_to_sync(billing.check_refunds)()
    async_to_sync(psql_async.engine_psql_async.dispose)()  