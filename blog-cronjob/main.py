import json
import logging
import os
import datetime
from celery import Celery
from kombu import Exchange, Queue
from log_handler import LambdaLogger

# Initialize Celery app with SQS as broker
broker_url = os.environ.get('CELERY_BROKER_URL', 'sqs://')
queue_name = os.environ['MESSAGE_QUEUE_NAME']
queue_url = os.environ['MESSAGE_QUEUE_URL']

celery_app = Celery('tasks', broker=broker_url)

# Configure Celery to use SQS
celery_app.conf.update(
    broker_transport_options={
        'region': 'ap-southeast-1',
        'predefined_queues': {
            queue_name: {
                'url': queue_url,
            }
        }
    },
    task_default_queue=queue_name,
    task_queues=(
        Queue(queue_name, Exchange(queue_name), routing_key=queue_name),
    )
)

logger = LambdaLogger(level=logging.INFO)
def lambda_handler(event, context):
    logger.info("Lambda function started", context=context, event=event)
    
    # NOTE: This must match the task_name configured in Celery workers
    DUMMY_TASK_NAME = "queue.dummy_task"
    IAM_BULK_CREATE_USER_TASK_DAILY_TASK_NAME = "iam.tasks.bulk_create_user_task_daily"

    
    if not queue_name:
        logger.error("MESSAGE_QUEUE_NAME environment variable is not set")
        return {
            'statusCode': 500,
            'body': json.dumps('Internal server error: MESSAGE_QUEUE_NAME not set')
        }
    
    logger.info(f"Received event", context=context, event=event)

    EVENT_TYPE_TO_TASK_NAME = {
        'DUMMY_TASK': DUMMY_TASK_NAME,
        'IAM_BULK_CREATE_USER_TASK_DAILY': IAM_BULK_CREATE_USER_TASK_DAILY_TASK_NAME,
    }
    event_type = event.get('EVENT_TYPE')
    
    # Get the task name based on the event type
    task_name = EVENT_TYPE_TO_TASK_NAME.get(event_type)

    if task_name is None:
        logger.error(f"Invalid event type: {event_type}", context=context, event=event)
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid event type')
        }
    
    try:
        result = celery_app.send_task(task_name, args=[], kwargs={}, queue=queue_name)
        log_message = "SENT {} {} {} {}".format(
            queue_name,
            task_name,
            result,
            -1,
        )
        logger.info(log_message, context=context, event=event)
    except Exception as e:
        logger.error(f"Error sending task to Celery: {e}", context=context, event=event)
        return {
            'statusCode': 500,
            'body': json.dumps(f'Internal server error: {str(e)}')
        }
    
    current_time = datetime.datetime.now().time()
    logger.info("Your cron function ran at " + str(current_time), context=context, event=event)
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Message sent to SQS. Res: {result}')
    }