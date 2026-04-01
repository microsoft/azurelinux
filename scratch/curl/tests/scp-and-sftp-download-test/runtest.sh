#!/bin/bash
# vim: dict=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of /CoreOS/curl/Sanity/scp-and-sftp-download-test
#   Description: downloads test file through scp and sftp
#   Author: Karel Srot <ksrot@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2012 Red Hat, Inc. All rights reserved.
#
#   This copyrighted material is made available to anyone wishing
#   to use, modify, copy, or redistribute it subject to the terms
#   and conditions of the GNU General Public License version 2.
#
#   This program is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE. See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public
#   License along with this program; if not, write to the Free
#   Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#   Boston, MA 02110-1301, USA.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Include Beaker environment
. /usr/share/beakerlib/beakerlib.sh || exit 1

PACKAGE="curl"

# GLOBAL/ENVIRONMENT VARIABLE:
# PUBKEY_PARAM

if [ "$PUBKEY_PARAM" == 'none' ]; then
  PUBKEY_PARAM=""
elif [ "$PUBKEY_PARAM" == 'empty' ]; then
  PUBKEY_PARAM="--pubkey ''"
else
  PUBKEY_PARAM='--pubkey /root/.ssh/id_rsa.pub'
fi

FILESIZE=200 #MB
OPTIONS=""
rlIsRHEL 7 && OPTIONS="--insecure"

rlJournalStart
    rlPhaseStartSetup
        rlAssertRpm $PACKAGE
        rlFileBackup --clean  /root/.ssh/known_hosts /root/.ssh
        rlFileBackup --clean  /etc/ssh/sshd_config
        rlRun "useradd -m curltestuser"

        # In FIPS-140 we need to explicitly allow one of libssh2-implemented
        # Kex algorithms (eg. DH14-SHA1).
        rlRun "echo 'KexAlgorithms +diffie-hellman-group14-sha1' >> /etc/ssh/sshd_config" 0
        rlServiceStop "sshd"
        rlRun "service sshd start && sleep 5" 0

        # file for download test
        rlRun "su - curltestuser -c 'dd if=/dev/zero of=testfile bs=1M count=200'" 0 "Creating $FILESIZE MB large test file"
        SUM=`sha256sum /home/curltestuser/testfile | cut -d ' ' -f 1`
        rlRun "TmpDir=\$(mktemp -d)" 0 "Creating tmp directory"
        rlRun "pushd $TmpDir"
        rlRun "rm -vf /root/.ssh/*"
        rlRun "ssh-keygen -t rsa -f /root/.ssh/id_rsa -N ''" 0 "Generate ssh key"
        rlRun "mkdir /home/curltestuser/.ssh && cat /root/.ssh/id_rsa.pub > /home/curltestuser/.ssh/authorized_keys && chown -R curltestuser.curltestuser /home/curltestuser/.ssh/" 0 "Save the key to .ssh/authorized_keys"

        # this is a workaround as libssh2 is not able to use newer hashes
        #rlRun "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/root/.ssh/known_hosts curltestuser@localhost 'exit'" 0 "First ssh login to add localhost to known_hosts"
        rlRun "ssh-keyscan localhost >>/root/.ssh/known_hosts"

        # files for upload test
        rlRun "dd if=/dev/zero of=uploadfile1 bs=1M count=50" 0 "Creating 50 MB large test file"
        UPSUM1=`sha256sum uploadfile1 | cut -d ' ' -f 1`
        rlRun "dd if=/dev/zero of=uploadfile2 bs=1M count=20" 0 "Creating 20 MB large test file"
        UPSUM2=`sha256sum uploadfile2 | cut -d ' ' -f 1`
    rlPhaseEnd

    rlPhaseStartTest "scp download test"
        rlRun "curl -o ./scp_file -u curltestuser: --key /root/.ssh/id_rsa $PUBKEY_PARAM $OPTIONS scp://localhost/home/curltestuser/testfile" 0 "Initiate curl scp download"
        rlAssertExists scp_file
        SCPSUM=`sha256sum ./scp_file | cut -d ' ' -f 1`
        rlAssertEquals "Checking that whole file was properly downloaded" $SUM $SCPSUM
        rm -f ./scp_file
    rlPhaseEnd

    rlPhaseStartTest "sftp download test"
        rlRun "curl -o ./sftp_file -u curltestuser: --key /root/.ssh/id_rsa $PUBKEY_PARAM $OPTIONS sftp://localhost/home/curltestuser/testfile" 0 "Initiate curl scp download"
        rlAssertExists sftp_file
        SFTPSUM=`sha256sum ./sftp_file | cut -d ' ' -f 1`
        rlAssertEquals "Checking that whole file was properly downloaded" $SUM $SFTPSUM
        rm -f ./sftp_file
    rlPhaseEnd

    rlPhaseStartTest "scp upload test"
        rlRun "curl -T '{uploadfile1,uploadfile2}' scp://localhost/home/curltestuser/ -u curltestuser: --key /root/.ssh/id_rsa $PUBKEY_PARAM $OPTIONS" 0 "Initiate curl scp upload"
        rlAssertExists /home/curltestuser/uploadfile1
        rlAssertExists /home/curltestuser/uploadfile2
        SCPUPSUM1=`sha256sum /home/curltestuser/uploadfile1 | cut -d ' ' -f 1`
        SCPUPSUM2=`sha256sum /home/curltestuser/uploadfile2 | cut -d ' ' -f 1`
        rlAssertEquals "Checking that 1st file was properly uploaded" ${UPSUM1} ${SCPUPSUM1}
        rlAssertEquals "Checking that 2nd file was properly uploaded" ${UPSUM2} ${SCPUPSUM2}
        rm -f /home/curltestuser/uploadfile1 /home/curltestuser/uploadfile2
    rlPhaseEnd

    rlPhaseStartTest "sftp upload test"
        rlRun "curl -T '{uploadfile1,uploadfile2}' sftp://localhost/home/curltestuser/ -u curltestuser: --key /root/.ssh/id_rsa $PUBKEY_PARAM $OPTIONS" 0 "Initiate curl sftp upload"
        rlAssertExists /home/curltestuser/uploadfile1
        rlAssertExists /home/curltestuser/uploadfile2
        SFTPUPSUM1=`sha256sum /home/curltestuser/uploadfile1 | cut -d ' ' -f 1`
        SFTPUPSUM2=`sha256sum /home/curltestuser/uploadfile2 | cut -d ' ' -f 1`
        rlAssertEquals "Checking that 1st file was properly uploaded" ${UPSUM1} ${SFTPUPSUM1}
        rlAssertEquals "Checking that 2nd file was properly uploaded" ${UPSUM2} ${SFTPUPSUM2}
        rm -f /home/curltestuser/uploadfile1 /home/curltestuser/uploadfile2
    rlPhaseEnd


    rlPhaseStartCleanup
        rlRun "userdel -r --force curltestuser"
        rlRun "popd"
        rlRun "rm -r $TmpDir" 0 "Removing tmp directory"
        rlFileRestore
        rlServiceRestore "sshd"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
