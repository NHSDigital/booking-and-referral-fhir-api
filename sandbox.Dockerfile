FROM python:3.7

WORKDIR /opt/app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY src .
COPY ../specification/booking-and-referral.yaml .

EXPOSE 9000
CMD ["python", "main.py"]
