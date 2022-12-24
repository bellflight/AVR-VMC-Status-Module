FROM docker.io/library/python:3.11 AS poetry-exporter

WORKDIR /work

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN python -m pip install poetry \
 && poetry export -o requirements.txt

FROM docker.io/library/python:3.11-bullseye

WORKDIR /app

COPY --from=poetry-exporter /work/requirements.txt requirements.txt

RUN python -m pip install pip wheel --upgrade && \
    python -m pip install -r requirements.txt

RUN apt-get update && apt-get install -y udev
RUN cp /usr/local/lib/python3.*/site-packages/Jetson/GPIO/99-gpio.rules /etc/udev/rules.d

COPY . .

CMD ["python", "thermal.py"]
