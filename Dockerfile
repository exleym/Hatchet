FROM python:3.7

RUN apt-get update

COPY requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt

COPY hatchet /app/hatchet
COPY config.py /app/config.py
COPY wsgi.py /app/
WORKDIR /app

CMD ["gunicorn", "-w 4", "wsgi:app"]
