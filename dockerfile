FROM python:3.7-slim-buster

COPY src/requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV CERTS_FOLDER /certificates
COPY src/ssl.conf ${CERTS_FOLDER}/ssl.conf
COPY src/generate_certificate.sh ${CERTS_FOLDER}/generate_certificate.sh
RUN chmod +x ${CERTS_FOLDER}/generate_certificate.sh

COPY src/main.py /app
RUN chmod +x /app/main.py

COPY docker_start.sh /app
RUN chmod +x /app/docker_start.sh

EXPOSE 4840

CMD ["./docker_start.sh"]