from celery import shared_task

@shared_task
def test_shared_task():
    """ Test for the celery task """

    print('TEST TASK IS RUNNING')
    return 'TEST TASK'
