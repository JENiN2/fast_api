FROM python:3.10-slim

WORKDIR /usr/app
COPY requirements.txt /usr/app
RUN pip install -r requirements.txt

COPY main.py blog_manager.py /usr/app/

ENTRYPOINT uvicorn main:app --host 0.0.0.0 --port 8000
