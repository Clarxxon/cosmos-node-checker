FROM python:3.8-slim-buster

# создание домашней дирректории
WORKDIR /code

# говорит py где лежит основной main пакет
ENV PYTHONPATH=/code/app

COPY requirements.txt /etc
RUN apt-get clean && apt-get update && apt-get install -y gcc && \
    pip install -r /etc/requirements.txt --no-cache-dir

COPY app/ /code/app
COPY init.sh /code

RUN chmod +x /code/init.sh

CMD ["/code/init.sh"]

EXPOSE 8000
