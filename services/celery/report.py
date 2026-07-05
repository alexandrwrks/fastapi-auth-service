from services.celery.main import celery_app



@celery_app.task
def hello_world():
    print('hello world')
