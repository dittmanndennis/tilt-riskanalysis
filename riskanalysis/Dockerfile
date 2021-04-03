FROM python:3.9-slim-buster

COPY . .

RUN pip install gunicorn
RUN pip install falcon

CMD [ "gunicorn", "-b", "0.0.0.0:8000", "app:api" ]