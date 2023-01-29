StartOnlineFedora:
    cd /home/admin/ClassMonitorTeacher
    git pull
    python3 manage.py migrate
    python3 manage.py makemigrations
    sudo systemctl reload nginx
    nohup gunicorn ClassMonitorTeacher.wsgi:application --bind 127.0.1.1:8001
