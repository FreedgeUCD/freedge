#!/bin/bash

openssl req -x509 -newkey rsa:2048 -keyout rsa_private.pem -nodes -out \
   rsa_cert.pem -subj "/CN=unused"
openssl pkcs8 -topk8 -inform PEM -outform DER -in rsa_private.pem \
   -nocrypt > rsa_private_pkcs8
