FROM python:3.7-slim-buster

WORKDIR /app

COPY src .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV CERTS_FOLDER /certificates

RUN chmod +x generate_certificate.sh
RUN chmod +x main.py

COPY docker_start.sh .
RUN chmod +x docker_start.sh

EXPOSE 4840

CMD ["./docker_start.sh"]