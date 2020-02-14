FROM python:3.6

RUN apt-get update -y && apt-get install -y vim curl supervisor

RUN mkdir -p /logs
COPY /supervisor/conf.d/supervisor.conf /etc/supervisor/conf.d/topic_handler.conf

RUN mkdir -p /app
COPY . /app

RUN cd /app && pip3 install -r requirements.txt

WORKDIR /app/

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
