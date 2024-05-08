#!/bin/bash
# vim: dict+=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of /CoreOS/opensc/Sanity/pkcs11-tool
#   Description: This is a sanity test for pkcs11-tool
#   Author: Jakub Jelen <jjelen@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2018 Red Hat, Inc.
#
#   This program is free software: you can redistribute it and/or
#   modify it under the terms of the GNU General Public License as
#   published by the Free Software Foundation, either version 2 of
#   the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE.  See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see http://www.gnu.org/licenses/.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Include Beaker environment
. /usr/share/beakerlib/beakerlib.sh || exit 1

PACKAGE="opensc"
## from OpenSC/src/tests/p11test/runtest.sh
SOPIN="12345678"
PIN="123456"
export GNUTLS_PIN=$PIN
GENERATE_KEYS=1
PKCS11_TOOL="pkcs11-tool"
NSSDB=db

function generate_cert() {
    TYPE="$1"
    ID="$2"
    LABEL="$3"

    # Generate key pair
    $PKCS11_TOOL --keypairgen --key-type="$TYPE" --login --pin=$PIN \
        --module="$P11LIB" --label="$LABEL" --id=$ID

    if [[ "$?" -ne "0" ]]; then
        echo "Couldn't generate $TYPE key pair"
        return 1
    fi

    # check type value for the PKCS#11 URI (RHEL7 is using old "object-type")
    TYPE_KEY="type"
    p11tool --list-all --provider="$P11LIB" --login | grep "object-type" && \
        TYPE_KEY="object-type"

    # Generate certificate
    certtool --generate-self-signed --outfile="$ID.cert" --template=cert.cfg \
        --provider="$P11LIB" --load-privkey "pkcs11:object=$LABEL;$TYPE_KEY=private" \
        --load-pubkey "pkcs11:object=$LABEL;$TYPE_KEY=public"
    # convert to DER:
    openssl x509 -inform PEM -outform DER -in "$ID.cert" -out "$ID.cert.der"
    # Write certificate
    #p11tool --login --write --load-certificate="$ID.cert" --label="$LABEL" \
    #    --provider="$P11LIB"
    $PKCS11_TOOL --write-object "$ID.cert.der" --type=cert --id=$ID \
        --label="$LABEL" --module="$P11LIB"

    rm "$ID.cert.der"

    # Extract public key, which is more digestible by some of the tools
    openssl x509 -inform PEM -in $ID.cert -pubkey > $ID.pub

    p11tool --login --provider="$P11LIB" --list-all
}

function card_setup() {
    case $1 in
        "softhsm")
            P11LIB="/usr/lib64/pkcs11/libsofthsm2.so"
            echo "directories.tokendir = .tokens/" > .softhsm2.conf
            echo "slots.removable = true" >> .softhsm2.conf
            echo "objectstore.backend = file" >> .softhsm2.conf
            echo "log.level = INFO" >> .softhsm2.conf
            mkdir ".tokens"
            export SOFTHSM2_CONF=".softhsm2.conf"
            # Init token
            softhsm2-util --init-token --slot 0 --label "SC test" --so-pin="$SOPIN" --pin="$PIN"
            ;;
        "opencryptoki")
            # Supports only RSA mechanisms
            P11LIB="/usr/lib64/pkcs11/libopencryptoki.so"
            SO_PIN=87654321
            SLOT_ID=3 # swtok slot
            rlServiceStart "pkcsslotd"
            echo "test_swtok" | /usr/sbin/pkcsconf -I -c $SLOT_ID -S $SO_PIN
            /usr/sbin/pkcsconf -u -c $SLOT_ID -S $SO_PIN -n $PIN
            ;;
        "libcacard")
            # Remove OpenSC from p11-kit so we do not recurse
            rlRun "rlFileBackup /usr/share/p11-kit/modules/"
            rlRun "rm /usr/share/p11-kit/modules/opensc.module"

            # we use softhsm internally
            rlRun "card_setup softhsm"

            # Setup NSS DB
            rlRun "mkdir $NSSDB"
            # Do not add a softhsm2 to the nssdb if there is already p11-kit-proxy
            rlRun "modutil -create -dbdir sql:$NSSDB -force"
            rlRun "modutil -list -dbdir sql:$NSSDB | grep 'library name: p11-kit-proxy.so'" 0,1
            if [ "$?" = "1" ]; then
                rlRun "modutil -force -add 'SoftHSM PKCS#11' -dbdir sql:$NSSDB -libfile $P11LIB"
            fi

            # Download and Install vsmartcard and virt_cacard
            rlRun "yes | dnf copr enable jjelen/vsmartcard"
            rlRun "dnf install -y virt_cacard virtualsmartcard"

            # Install the temporary SELinux policy
            rlRun "semodule -i virtcacard.cil"

            # Restart pcscd
            rlRun "systemctl restart pcscd"

            # Start virtcacard
            #rlRun "G_MESSAGES_DEBUG=libcacard LIBCACARD_DEBUG=1 ./virt_cacard/virt_cacard 2> virt_cacard.debug &"
            rlRun "/usr/bin/virt_cacard 2> virt_cacard.debug &"
            rlRun "sleep 5"

            # We will use OpenSC directly from here
            P11LIB="/usr/lib64/pkcs11/opensc-pkcs11.so"

            rlRun "$PKCS11_TOOL -O"

            # The keys are already generated in softhsm
            return 0
            ;;
        *)
            echo "Error: Missing argument."
            exit 1;
            ;;
    esac

    if [[ $GENERATE_KEYS -eq 1 ]]; then
        # Generate 1024b RSA Key pair
        generate_cert "RSA:1024" "0001" "RSA1024"
        # Generate 2048b RSA Key pair
        generate_cert "RSA:2048" "0002" "RSA2048"
        # Generate 3092b RSA Key pair
        generate_cert "RSA:2048" "0003" "RSA3"
    fi
}

function card_cleanup() {
    case $1 in
        "softhsm")
            rm .softhsm2.conf
            rm -rf ".tokens"
            ;;
        "libcacard")
            rlRun "pkill virt_cacard" 0,1
            rlFileSubmit virt_cacard.debug
            rlRun "rm -rf $NSSDB"
            card_cleanup softhsm
            rlRun "rlFileRestore"
            ;;
    esac
    if [[ $GENERATE_KEYS -eq 1 ]]; then
        rm "0{1,2,3,4}.{cert,pub}"
    fi
}


rlJournalStart
    rlPhaseStartSetup "General setup"
        rlAssertRpm $PACKAGE
    rlPhaseEnd

    for BACKEND in "softhsm" "opencryptoki" "libcacard"; do
        rlPhaseStartSetup "Set up $BACKEND"
            rlAssertRpm $BACKEND
            rlRun "TmpDir=\$(mktemp -d)" 0 "Creating tmp directory"
            rlRun "cp cert.cfg virtcacard.cil $TmpDir"
            rlRun "pushd $TmpDir"
            rlRun "card_setup $BACKEND"
            rlRun 'echo "data to sign (max 100 bytes)" > data'
            # Read the certificates from the module (the IDs might get mixed up in libcacard)
            for ID in "0001" "0002" "0003"; do
                rlRun ">$ID.cert"
                rlRun "$PKCS11_TOOL --read-object --id $ID --type cert --output-file $ID.cert --module $P11LIB"
                rlRun "openssl x509 -inform DER -in $ID.cert -pubkey > $ID.pub"
            done
        rlPhaseEnd

        for HASH in "" "SHA1" "SHA224" "SHA256" "SHA384" "SHA512"; do
            for SIGN_KEY in "0001" "0002" "0003"; do
                METHOD="RSA-PKCS"
                if [[ ! -z $HASH ]]; then
                    METHOD="$HASH-$METHOD"
                fi
                # OpenCryptoki does not work with hashed mechanisms
                if [[ "$BACKEND" != "opencryptoki" ]]; then
                    rlPhaseStartTest "$BACKEND: $METHOD: Sign & Verify (KEY $SIGN_KEY)"
                        rlRun "$PKCS11_TOOL --id $SIGN_KEY -s -p $PIN -m $METHOD --module $P11LIB \
                               --input-file data --output-file data.sig"

                        # OpenSSL verification
                        if [[ -z $HASH ]]; then
                            rlRun "openssl rsautl -verify -pubin -inkey $SIGN_KEY.pub -in data.sig"
                        else
                            rlRun "openssl dgst -verify $SIGN_KEY.pub -${HASH,,*} \
                                   -signature data.sig data"
                        fi

                        # pkcs11-tool verification
                        rlRun "$PKCS11_TOOL --id $SIGN_KEY --verify -m $METHOD --module $P11LIB \
                               --input-file data --signature-file data.sig"
                        rlRun "rm data.sig"
                    rlPhaseEnd
                fi

                METHOD="$METHOD-PSS"
                if [[ "$HASH" == "SHA512" ]]; then
                    continue; # This one is broken
                fi
                rlPhaseStartTest "$BACKEND: $METHOD: Sign & Verify (KEY $SIGN_KEY)"
                    if [[ -z $HASH ]]; then
                        # hashing is done outside of the module. We chose here SHA256
                        rlRun "openssl dgst -binary -sha256 data > data.hash"
                        HASH_ALGORITM="--hash-algorithm=SHA256"
                        VERIFY_DGEST="-sha256"
                        VERIFY_OPTS="-sigopt rsa_mgf1_md:sha256"
                    else
                        # hashing is done inside of the module
                        rlRun "cp data data.hash"
                        HASH_ALGORITM=""
                        VERIFY_DGEST="-${HASH,,*}"
                        VERIFY_OPTS="-sigopt rsa_mgf1_md:${HASH,,*}"
                    fi
                    rlRun "$PKCS11_TOOL --id $SIGN_KEY -s -p $PIN -m $METHOD --module $P11LIB \
                           $HASH_ALGORITM --salt-len=-1 \
                           --input-file data.hash --output-file data.sig"

                    # OpenSSL verification
                    rlRun "openssl dgst -verify $SIGN_KEY.pub $VERIFY_DGEST \
                           -sigopt rsa_padding_mode:pss  $VERIFY_OPTS -sigopt rsa_pss_saltlen:-1 \
                           -signature data.sig data"

                    # pkcs11-tool verification
                    rlRun "$PKCS11_TOOL --id $SIGN_KEY --verify -m $METHOD --module $P11LIB \
                           $HASH_ALGORITM --salt-len=-1 \
                           --input-file data.hash --signature-file data.sig"
                    rlRun "rm data.{sig,hash}"

                rlPhaseEnd
            done

            # Skip hashed algorithms (do not support encryption & decryption)
            if [[ ! -z "$HASH" ]]; then
                continue;
            fi
            METHOD="RSA-PKCS"
            for ENC_KEY in "0001" "0002" "0003"; do
                rlPhaseStartTest "$BACKEND: $METHOD: Encrypt & Decrypt (KEY $ENC_KEY)"
                    # OpenSSL Encryption
                    rlRun "openssl rsautl -encrypt -pubin -inkey $ENC_KEY.pub -in data \
                           -out data.crypt"
                    rlRun "$PKCS11_TOOL --id $ENC_KEY --decrypt -p $PIN -m $METHOD \
                           --module $P11LIB --input-file data.crypt > data.decrypted"
                    rlRun "diff data{,.decrypted}"
                    rlRun "rm data.{crypt,decrypted}"

                    # TODO pkcs11-tool encryption
                rlPhaseEnd
            done
        done

        rlPhaseStartCleanup "Cleanup $BACKEND"
            card_cleanup $BACKEND
            rlRun "popd"
            rlRun "rm -r $TmpDir" 0 "Removing tmp directory"
        rlPhaseEnd
    done
rlJournalPrintText
rlJournalEnd
