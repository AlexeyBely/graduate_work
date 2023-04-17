import logging
from asgiref.sync import async_to_sync
from celery import Celery

from core.config import settings
from billing.billing_offer import get_billing_offer
from billing.privileged_role import subscribe_roles
from crud_service.crud_dependency import get_crud_billing, get_crud_marketing
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
    # Periodic task 15c
    sender.add_periodic_task(15.0, 
                             load_payment_system.s(), 
                             name='load from payment system')    
    # Periodic task 25c
    sender.add_periodic_task(25.0, 
                             check_subscribe.s(), 
                             name='check subscription expiration')


@app.task
def load_payment_system():
    """Check payments and refunds in payment system."""
    billing = get_billing_offer()
    async_to_sync(billing.check_payments)()
    async_to_sync(billing.check_refunds)()
    async_to_sync(psql_async.engine_psql_async.dispose)()


@app.task
def check_subscribe():
    """Check subscription expiration."""
    crud_marketing = get_crud_marketing()
    crud_billing = get_crud_billing()
    roles_service = subscribe_roles(crud_marketing, crud_billing)
    async_to_sync(roles_service.check_end_subscribe)()
    async_to_sync(psql_async.engine_psql_async.dispose)() 
