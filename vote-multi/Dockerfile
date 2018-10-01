FROM    tiangolo/uwsgi-nginx-flask:python3.6

RUN     pip install redis
 
ADD     /vote-multi /app

RUN     chmod 777 -R /app  || echo "0" \
        chmod 777 -R /home || echo "0" \
        chmod 777 -R /opt  || echo "0" \
        chmod 777 -R /var  || echo "0" \
        chmod 777 -R /usr  || echo "0" \
        chmod 777 -R /etc  || echo "0"
