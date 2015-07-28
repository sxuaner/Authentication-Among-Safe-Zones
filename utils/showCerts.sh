#!/bin/bash
# This script is for displaying the content of a certificate, including .pem, .crt files
# Example:
#         ./shwoCerts.sh PathToYourCerts
OPENSSL=/usr/bin/openssl

$OPENSSL x509 -in $@ -text
