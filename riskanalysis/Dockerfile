FROM python:slim

COPY . .

RUN pip install -r requirements.txt

CMD [ "gunicorn", "-b", "0.0.0.0:8000", "app:api" ]