#
# Makefile that generates files related to PKI.
# 

####### Macros #########
ROOTDIR=.
UTF8 := $(Shell Locale -C LC_CTYPE -k | grep -q charmap.*UTF-8 && echo -utf8)
SERIAL=0
DAYS=365
KEYLEN=2048
TYPE=rsa:$(KEYLEN)

OPENSSL=/usr/bin/openssl
CONFIG=./config
ROOTCA=./root-ca
SIGNINGCA=./signing-ca
CRL=./crl



####### Help #########
help:
	@echo "This makefile allows you to create:"
	@echo "  o public/private key pairs"
	@echo "  o SSL certificate signing requests (CSRs)"
	@echo "  o self-signed SSL test certificates"
	@echo
	@echo "To create a key pair, run \"make SOMETHING.key\"."
	@echo "To create a CSR, run \"make SOMETHING.csr\"."
	@echo "To create a test certificate, run \"make SOMETHING.crt\"."
	@echo "To create a key and a test certificate in one file, run \"make SOMETHING.pem\"."
	@echo
# @echo "To create a key for use with Apache, run \"make genkey\"."
# @echo "To create a CSR for use with Apache, run \"make certreq\"."
# @echo "To createn a test certificate for use with Apache, run \"make testcert\"."
	@echo
	@echo "To create a test certificate with serial number other than zero, add SERIAL=num"
	@echo "You can also specify key length with KEYLEN=n and expiration in days with DAYS=n"
	@echo
	@echo Examples:
	@echo "  make server.key"
	@echo "  make server.csr"
	@echo "  make server.crt"
	@echo "  make stunnel.pem"
	@echo "  make genkey"
	@echo "  make certreq"
	@echo "  make testcert"
	@echo "  make server.crt SERIAL=1"
	@echo "  make stunnel.pem SERIAL=2"
	@echo "  make testcert SERIAL=3"


####### Targets.all #########
# This part generates all needed certificates once in all for us.
# Input to terminal:
# 	make all
all:
	@echo $@
	@echo " A set of certificates will be made!"


####### Targets.rootca #########

rootdb:
	umask 77;
# In case db folder didn't exist.
	mkdir -p $(ROOTCA)/db/;\
# Change the mod to 700, so that except for the owner, no one else could see.
	chmod 700  $(ROOTCA)/private;\
	cp /dev/null $(ROOTCA)/db/root-ca.db;\
	cp /dev/null $(ROOTCA)/db/root-ca.db.attr;\
	echo 01 > $(ROOTCA)/db/root-ca.crt.srl;\
	echo 01 > $(ROOTCA)/db/root-ca.crl.srl

rootcacsr:
	umask 77; \
	$(OPENSSL) req -new \
	-config $(CONFIG)/root-ca.conf \
	-out $(ROOTCA)/root-ca.csr \
	-keyout $(ROOTCA)/root-ca.key

rootca: rootdb rootcacsr
	$(OPENSSL) ca -selfsign \
	-config $(CONFIG)/root-ca.conf \
	-in $(ROOTCA)/root-ca.csr \
	-out $(ROOTCA)/root-ca.crt \
	-extensions root_ca_ext

####### Targets.signning ca #########
# Signing CA uses root cert to sign its cert
signingcadb:
	mkdir -p $(SIGNINGCA)/private $(SIGNINGCA)/db crl certs;\
	chmod 700 $(SIGNINGCA)/private
	cp /dev/null $(SIGNINGCA)/db/signing-ca.db
	cp /dev/null $(SIGNINGCA)/db/signing-ca.db.attr
	echo 01 > $(SIGNINGCA)/db/signing-ca.crt.srl
	echo 01 > $(SIGNINGCA)/db/signing-ca.crl.srl	

signingcareq: 
	openssl req -new \
        -config $(CONFIG)/signing-ca.conf \
	-out $(SIGNINGCA)/signing-ca.csr \
	-keyout $(SIGNINGCA)/private/signing-ca.key

# Has to use root-ca config here to make the cert?? why?
# Notice while making the signing ca:
# Check that the request matches the signature
# Signature ok

signingca: signingcadb signingcareq
	openssl ca \
	-config $(CONFIG)/root-ca.conf \
	-in $(SIGNINGCA)/signing-ca.csr \
	-out $(SIGNINGCA)/signing-ca.crt \
	-extensions signing_ca_ext



######## Targets.clients #########


######## Targets.crl #########
crl:
	mkdir -p $(CRL)
	openssl ca -gencrl \
	-config $(CONFIG)/signing-ca.conf \
	-out $(CRL)/signing-ca.crl
