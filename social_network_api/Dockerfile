FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/


RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 9000/tcp

RUN python manage.py collectstatic --noinput

CMD ["python", "manage.py", "runserver", "0.0.0.0:9000", "--insecure"]