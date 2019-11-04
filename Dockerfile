FROM python:3.7
MAINTAINER Roman Peters "mqtt-hawk@romanpeters.nl"
COPY . /app
COPY ./config.yaml.example /app/config.yaml
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "mqtthawk"]
