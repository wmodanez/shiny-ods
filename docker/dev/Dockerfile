FROM python:latest

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get upgrade -y --allow-unauthenticated

WORKDIR /home/shiny

COPY ods/* ./
RUN python3 -m venv /opt/venv

RUN . /opt/venv/bin/activate && pip install -r requirements.txt

EXPOSE 8080

CMD . /opt/venv/bin/activate && exec python myapp.py