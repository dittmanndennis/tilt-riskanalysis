FROM python:3.9-slim-buster

COPY . .

RUN gunicorn --worker-tmp-dir /dev/shm ...
RUN gunicorn --workers=2 --threads=4 --worker-class=gthread
RUN gunicorn --log-file=- ...
CMD [ "gunicorn", "-b", "0.0.0.0:8000", "app:api" ]