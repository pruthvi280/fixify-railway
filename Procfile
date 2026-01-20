web: cd Web_App && gunicorn main:app --bind 0.0.0.0:$PORT
worker: cd Web_App && celery -A Backend.celery.worker.celery_app worker --loglevel=info
beat: cd Web_App && celery -A Backend.celery.worker.celery_app beat --loglevel=info