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


####### Targets #########

all:
	@echo $@
	@echo " A set of certificates will be made!"

####### Targets.create #########

%.pem:
	umask 77 ; \
	PEM1=`/bin/mktemp /tmp/openssl.XXXXXX` ; \
	PEM2=`/bin/mktemp /tmp/openssl.XXXXXX` ; \
	$(OPENSSL) req $(UTF8) -newkey $(TYPE) -keyout $$PEM1 -nodes -x509 -days $(DAYS) -out $$PEM2 -set_serial $(SERIAL) ; \
	cat $$PEM1 >  $@ ; \
	echo ""    >> $@ ; \
	cat $$PEM2 >> $@ ; \
# 	rm $$PEM1 $$PEM2

%.key:
	umask 77 ; \
	$(OPENSSL) genrsa -aes128 $(KEYLEN) > $@

%.csr: %.key
	umask 77 ; \
	$(OPENSSL) req $(UTF8) -new -key $^ -out $@

%.crt: %.key
	umask 77 ; \
	$(OPENSSL) req $(UTF8) -new -key $^ -x509 -days $(DAYS) -out $@ -set_serial $(SERIAL)

genkey: $(KEY)
certreq: $(CSR)
testcert: $(CRT)

$(CSR): $(KEY)
	umask 77 ; \
	/usr/bin/openssl req $(UTF8) -new -key $(KEY) -out $(CSR)

$(CRT): $(KEY)
	umask 77 ; \
	/usr/bin/openssl req $(UTF8) -new -key $(KEY) -x509 -days $(DAYS) -out $(CRT) -set_serial $(SERIAL)

####### Targets.display #########
show:
	$(OPENSSL) x509 -in my-ca.crt -text -noout


####### Targets.clean #########
clean:
	@echo "Nothing to clean yet!"

