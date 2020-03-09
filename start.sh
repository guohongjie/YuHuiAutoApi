#!/bin/bash
celery_log="celery.log"
uwsgi_log="uwsgi.log"
if [ ! -f "${celery_log}"]; then
echo "celery.log 文件不存在";
else
rm celery.log;
fi;
if [ ! -f "${uwsgi_log}"]; then
echo "uwsgi.log 文件不存在";
else
rm uwsgi.log;
fi;
echo "启动uwsgi.ini文件"
uwsgi uwsgi.ini &
echo "启动celery_task任务"
nohup celery -A  manage.celery worker --loglevel=info > celery.log &
exit