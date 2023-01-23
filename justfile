StartOnlineFedora:
    cd /home/admin/ClassMonitorTeacher
    git pull
    sudo systemctl reload nginx
    nohup gunicorn ClassMonitorTeacher.wsgi:application --bind 0.0.0.0:8001
