from celery import Celery

app = Celery('vote',
             broker='redis://localhost:6379',
             backend='cache://',
             include=['vote.tasks'])


if __name__ == '__main__':
    app.start()
