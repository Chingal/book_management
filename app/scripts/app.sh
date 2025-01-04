#!/bin/bash
mkdir /home/app/logs > /dev/null 2>&1

touch /home/app/logs/gunicorn-access.log
touch /home/app/logs/gunicorn.log
#touch /home/app/logs/app.log
tail -n 0 -f /home/app/logs/*.log &

python manage.py collectstatic --clear --noinput > /dev/null 2>&1
python manage.py collectstatic --noinput > /dev/null 2>&1

exec gunicorn $PROJECT_NAME.wsgi -w 2 -b :8007 \
    --access-logfile /home/app/logs/gunicorn-access.log \
    --error-logfile /home/app/logs/gunicorn.log --reload \
    --capture-output