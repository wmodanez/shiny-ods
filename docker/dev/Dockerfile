FROM python:latest

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get upgrade -y --allow-unauthenticated
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y libsodium-dev python3 python3-pip python3-venv

WORKDIR /home/shiny

COPY ods/* ./

RUN pip3 install --break-system-packages --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8080

CMD ["shiny", "run --reload", "app.py", "--host", "0.0.0.0", "--port", "8080"]
