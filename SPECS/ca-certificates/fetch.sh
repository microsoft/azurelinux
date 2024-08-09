#!/bin/sh
#
# This script fetches the latest released certdata.txt and updates the 
# ca-certificates.spec file
#
baseurl="https://hg.mozilla.org/releases/mozilla-release/raw-file/default/security/nss/lib"
force=0
release_type="RTM"
release="3_43"
while [ -n "$1" ]; do
   case $1 in
   "-d")
	baseurl="https://hg.mozilla.org/projects/nss/raw-file/default/lib"
	;;
   -t*)
	release_type=`echo $1 | sed -e 's;-t;;'`
	if [ "${release_type}" = "" ]; then
	   shift
	   release_type=$1
	fi
	baseurl="https://hg.mozilla.org/projects/nss/raw-file/NSS_${release}_${release_type}/lib"
	;;
   -n*)
	release=`echo $1 | sed -e 's;-n;;'`
	if [ "${release}" = "" ]; then
	   shift
	   release=$1
	fi
	release=`echo ${release} | sed -e 's;\\.;_;g'`
	baseurl="https://hg.mozilla.org/projects/nss/raw-file/NSS_${release}_${release_type}/lib"
	;;
   "-f")
	force=1
	;;
    *)
	echo "usage: $0 [-r] [-n release] [-f]"
	echo "-d           use the development tip rather than the latest release"
	echo "-n release   fetch a specific nss release"
	echo "-f           skip the verify check"
	exit 1
	;;
    esac
    shift
done

# get the current certdata version number
# nss version number
# user making the change
# email of user
# 
# versions from the latest nss code in mozilla
echo "Getting CKBI version number"
ckbi_version=`wget ${baseurl}/ckfw/builtins/nssckbi.h -O - | grep "NSS_BUILTINS_LIBRARY_VERSION " | awk '{print $NF}' | sed -e "s;\";;g" `
if [ "${ckbi_version}" = "" ]; then
    echo "Didn't find ckbi version from ${baseurl}"
    exit 1;
fi
echo "Getting NSS version number"
nss_version=`wget ${baseurl}/nss/nss.h -O - | grep "NSS_VERSION" | awk '{print $3}' | sed -e "s;\";;g" `
if [ "${nss_version}" = "" ]; then
    echo "Didn't find nss version from ${baseurl}"
    exit 1;
fi
# date from the current system date on this machine
echo "Creating change log"
export LANG=C
year=`date +%Y`
log_date=`date +"%a %b %d %Y"`
# user name from the environment, fallback to git, fallback to the current user
username=`whoami`
name=${NAME}
if [ "${name}" = "" ]; then
   name=`git config user.name`
fi
if [ "${name}" = "" ]; then
   name=`getent passwd $username`
fi
email=${EMAIL}
if [ "${email}" = "" ]; then
   email=`git config user.email`
fi
if [ "${email}" = "" ]; then
   email=$username@`hostname`
fi
# rawhide >=2, branches 1.x
cwd=$(pwd)
if [ `basename ${cwd}` = master ]; then
    release="2"
else
    release="1.0"
fi
version=${year}.${ckbi_version}

#make sure the the current version is newer than what is already there
current_version=`grep ^Version: ca-certificates.spec | awk '{ print $NF }'`
if [ ${current_version} \> ${version} -o ${current_version} = ${version} ]; then
   echo "Can't downgrade current version: ${current_version} new version: ${version}"
   exit 1;
fi

# now get our new certdata.txt
echo "Fetching new certdata.txt"
wget ${baseurl}/ckfw/builtins/certdata.txt -O certdata.txt
if [ $? -ne 0 ]; then
   echo fetching certdata.text from ${baseurl} failed!
   echo " To restore the old certdata.txt use:"
   echo "    git checkout -- certdata.txt"
   exit 1;
fi

# Verify everything is good with the user
echo -e "Upgrading ${current_version} -> ${version}:"
echo -e "*${log_date} ${name} <$email> ${version}-${release}\n - Update to CKBI ${ckbi_version} from NSS ${nss_version}"
./check_certs.sh
echo ""

yn=""
if [ ! ${force} ]; then
	echo -n "Do you want to continue (Y/N default Y)? "
	read yn
	echo ""
fi
if [ "${yn}" != "" -a "${yn}" != "y" -a "${yn}" != "Y" -a "${yn}" != "yes" -a "${yn}" != "YES" ]; then
    echo "Skipping ca-certificate.spec upgrade."
    echo " NOTE: certdata.txt has been upgraded."
    echo " To restore the old certdata.txt use:"
    echo "    git checkout -- certdata.txt"
    exit 1;
fi

echo "Updating .spec file"
cat ca-certificates.spec | while IFS= read -r line
do
    echo $line | grep "^Version: " 1>&2
    if [ $? -eq 0 ]; then
	echo "Version: ${version}"
	echo "New Version: ${version}" 1>&2
	continue
    fi
    echo $line | grep "^Release: " 1>&2
    if [ $?  -eq 0 ]; then
	echo "Release: ${release}%{?dist}"
	echo "New Release: ${release}%{?dist}" 1>&2
	continue
    fi
    echo $line | grep "^%changelog" 1>&2
    if [ $?  -eq 0 ]; then
	echo "$line"
	echo -e "*${log_date} ${name} <$email> ${version}-${release}\n - Update to CKBI ${ckbi_version} from NSS ${nss_version}"
	echo -e "*${log_date} ${name} <$email> ${version}-${release}\n - Update to CKBI ${ckbi_version} from NSS ${nss_version}"  1>&2
	./check_certs.sh
       echo ""
	continue
    fi
    echo "$line"
done > /tmp/ca-certificates.spec.$$
mv /tmp/ca-certificates.spec.$$ ca-certificates.spec
git status
exit 0
