#!/usr/bin/env bash

# TODO: WIP only use it as a reference. From this article: https://aws.amazon.com/blogs/compute/introducing-mutual-tls-authentication-for-amazon-api-gateway/

openssl genrsa -out RootCA.key 4096
openssl req -new -x509 -days 3650 -key RootCA.key -out RootCA.pem

openssl genrsa -out my_client.key 2048
openssl req -new -key my_client.key -out my_client.csr

openssl x509 -req -in my_client.csr -CA RootCA.pem -CAkey RootCA.key -set_serial 01 -out my_client.pem -days 3650 -sha256

cp RootCA.pem truststore.pem

# Produces 403 Forbidden
curl -X GET --key my_client.key --cert my_client.pem -i https://jaho3.bars.dev.api.platform.nhs.uk/mock-receiver/Appointment
