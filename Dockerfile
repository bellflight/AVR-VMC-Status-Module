FROM docker.io/library/python:3.11-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python -m pip install pip wheel --upgrade && \
    python -m pip install -r requirements.txt

RUN apt-get update && apt-get install -y udev
RUN cp /usr/local/lib/python3.11/site-packages/Jetson/GPIO/99-gpio.rules /etc/udev/rules.d

COPY . .

CMD ["python", "thermal.py"]
