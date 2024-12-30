cd /mnt/c/MyProjects/chat-police/backend
./venv/bin/python3 -m celery -A settings beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
