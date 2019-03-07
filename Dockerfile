FROM python:3.7
MAINTAINER Roman Peters "mqtt-hawk@romanpeters.nl"
COPY . /mqtt-hawk
WORKDIR /mqtt-hawk
RUN pip install -r requirements.txt

CMD ["python", "mqtthawk"]
