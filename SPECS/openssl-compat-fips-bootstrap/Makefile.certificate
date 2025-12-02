UTF8 := $(shell locale -c LC_CTYPE -k | grep -q charmap.*UTF-8 && echo -utf8)
DAYS=365
KEYLEN=2048
TYPE=rsa:$(KEYLEN)
EXTRA_FLAGS=
ifdef SERIAL
	EXTRA_FLAGS+=-set_serial $(SERIAL)
endif

.PHONY: usage
.SUFFIXES: .key .csr .crt .pem
.PRECIOUS: %.key %.csr %.crt %.pem

usage:
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
	@echo "To create a key for use with Apache, run \"make genkey\"."
	@echo "To create a CSR for use with Apache, run \"make certreq\"."
	@echo "To create a test certificate for use with Apache, run \"make testcert\"."
	@echo
	@echo "To create a test certificate with serial number other than random, add SERIAL=num"
	@echo "You can also specify key length with KEYLEN=n and expiration in days with DAYS=n"
	@echo "Any additional options can be passed to openssl req via EXTRA_FLAGS"
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
	@echo "  make stunnel.pem EXTRA_FLAGS=-sha384"
	@echo "  make testcert DAYS=600"

%.pem:
	umask 77 ; \
	PEM1=`/bin/mktemp /tmp/openssl.XXXXXX` ; \
	PEM2=`/bin/mktemp /tmp/openssl.XXXXXX` ; \
	/usr/bin/openssl req $(UTF8) -newkey $(TYPE) -keyout $$PEM1 -nodes -x509 -days $(DAYS) -out $$PEM2 $(EXTRA_FLAGS) ; \
	cat $$PEM1 >  $@ ; \
	echo ""    >> $@ ; \
	cat $$PEM2 >> $@ ; \
	$(RM) $$PEM1 $$PEM2

%.key:
	umask 77 ; \
	/usr/bin/openssl genrsa -aes128 $(KEYLEN) > $@

%.csr: %.key
	umask 77 ; \
	/usr/bin/openssl req $(UTF8) -new -key $^ -out $@

%.crt: %.key
	umask 77 ; \
	/usr/bin/openssl req $(UTF8) -new -key $^ -x509 -days $(DAYS) -out $@ $(EXTRA_FLAGS)

TLSROOT=/etc/pki/tls
KEY=$(TLSROOT)/private/localhost.key
CSR=$(TLSROOT)/certs/localhost.csr
CRT=$(TLSROOT)/certs/localhost.crt

genkey: $(KEY)
certreq: $(CSR)
testcert: $(CRT)

$(CSR): $(KEY)
	umask 77 ; \
	/usr/bin/openssl req $(UTF8) -new -key $(KEY) -out $(CSR)

$(CRT): $(KEY)
	umask 77 ; \
	/usr/bin/openssl req $(UTF8) -new -key $(KEY) -x509 -days $(DAYS) -out $(CRT) $(EXTRA_FLAGS)
