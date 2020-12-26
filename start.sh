ps -efww| grep app:app | grep -v grep | cut -c 9-15|xargs kill -9
cd application
/usr/bin/python3 /usr/local/bin/gunicorn -b 0.0.0.0:8080 app:app &
docker run -p 81:8080 -e SWAGGER_JSON=/api.yaml -v /root/pony/openapi/api.yaml:/api.yaml swaggerapi/swagger-ui &