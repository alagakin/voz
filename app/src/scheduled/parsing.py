from celery_config import app


@app.task
def parse():
    print('parsing')
