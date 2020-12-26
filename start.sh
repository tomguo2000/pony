ps -efww| grep app:app | grep -v grep | cut -c 9-15|xargs kill -9
cd application
/usr/bin/python3 /usr/local/bin/gunicorn -b 0.0.0.0:8080 app:app &
