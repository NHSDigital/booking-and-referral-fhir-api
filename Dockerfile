FROM python:3.7

WORKDIR /opt/app

COPY sandbox/requirements.txt .

RUN pip3 install -r requirements.txt

COPY sandbox/src .
COPY specification/examples routes/examples

EXPOSE 9000
CMD ["python", "main.py"]
