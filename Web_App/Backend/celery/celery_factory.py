from celery import Celery, Task
from flask import Flask
import os

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)

    # DIRECT FIX: Use REDIS_URL directly instead of looking for "CELERY" dict
    redis_url = app.config.get("REDIS_URL", os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/0"))

    celery_app.conf.update(
        broker_url=redis_url,
        result_backend=redis_url,
        task_ignore_result=True,
    )

    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
