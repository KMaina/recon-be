FROM python:3.7

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY ./start.sh /start.sh

RUN chmod +x /start.sh

COPY ./app /app

CMD ["./start.sh"]