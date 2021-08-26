FROM python:3.7

WORKDIR /opt/app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY src .

CMD ["python", "mock_api.py"]
