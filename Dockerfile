FROM python:3.10-bullseye

COPY ./app /app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -r /app/requirements.txt
CMD [ "python", "main.py" ]