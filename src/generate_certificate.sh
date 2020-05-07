#!/bin/bash 

SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_FOLDER=$(dirname "$SCRIPT_PATH")

KEY_FILE_PATH="$SCRIPT_FOLDER/key.pem"
SSL_FILE_PATH="$SCRIPT_FOLDER/ssl.conf"
CERTIFICATE_PEM_FILE_PATH="$SCRIPT_FOLDER/certificate.pem"
CERTIFICATE_DER_FILE_PATH="$SCRIPT_FOLDER/certificate.der"

if [ -f $KEY_FILE_PATH ]; then
    echo "$KEY_FILE_PATH file already exists!"
    exit
fi

if [ -f $CERTIFICATE_DER_FILE_PATH ]; then
    echo "$CERTIFICATE_DER_FILE_PATH file already exists!"
    exit
fi

if [ ! -f $SSL_FILE_PATH ]; then
    echo "$SSL_FILE_PATH does not exists!"
    exit
fi

openssl genrsa -out $KEY_FILE_PATH 2048
openssl req -x509 -days 365 -new -out $CERTIFICATE_PEM_FILE_PATH -key $KEY_FILE_PATH -config $SSL_FILE_PATH
openssl x509 -outform der -in $CERTIFICATE_PEM_FILE_PATH -out $CERTIFICATE_DER_FILE_PATH