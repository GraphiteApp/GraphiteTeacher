StartOnlineFedora:
    cd /home/archons/GraphiteTeacher
    git pull
    python3 manage.py migrate
    python3 manage.py makemigrations
    sudo systemctl reload nginx
    nohup gunicorn GraphiteTeacher.wsgi:application --bind 127.0.1.1:8001
