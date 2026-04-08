#!/bin/bash
#
# Create Red Hat OpenJDK security properties directory hierarchy.
#
# Copyright (C) 2025 IBM Corporation. All rights reserved.
#
# Written by:
#     Francisco Ferrari Bihurriet <fferrari@redhat.com>
#     Thomas Fitzsimmons <fitzsim@redhat.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Usage:
#
# bash create-redhat-properties-files.bash <target directory> <nssadapter path>
#
# Example usage in spec file:
#
# bash -x create-redhat-properties-files.bash ${installdir}/conf/security \
#     %{_libdir}/%{sdkdir -- ${suffix}}/libnssadapter.so
#
# When you make changes to the file set here, also update the %files
# section in the spec file, and the JDK_PROPS_FILES_JDK_25 variables
# in TestSecurityProperties.java.

[[ $# == 2 ]] || exit 1

SECURITY="${1}"
NSSADAPTER="${2}"
VENDOR="${SECURITY}"/redhat
install --directory --mode=755 "${VENDOR}"
install --directory --mode=755 "${VENDOR}"/true
install --directory --mode=755 "${VENDOR}"/false

# /usr/lib/jvm/java-25-openjdk/conf/security/redhat/SunPKCS11-FIPS.cfg
install --mode 644 /dev/stdin "${VENDOR}"/SunPKCS11-FIPS.cfg <<EOF
name = FIPS
library = ${NSSADAPTER}
slot = 3
nssUseSecmod = false
attributes(*,CKO_SECRET_KEY,*)={ CKA_SIGN=true CKA_ENCRYPT=true }
EOF

# /usr/lib/jvm/java-25-openjdk/conf/security/redhat/false/crypto-policies.properties
install --mode 644 /dev/stdin "${VENDOR}"/false/crypto-policies.properties <<'EOF'
# Empty on purpose, for ${redhat.crypto-policies}=false
EOF

# /usr/lib/jvm/java-25-openjdk/conf/security/redhat/true/crypto-policies.properties
install --mode 644 /dev/stdin "${VENDOR}"/true/crypto-policies.properties <<'EOF'
#
# Apply the system-wide crypto policy
#
include /etc/crypto-policies/back-ends/java.config

#
# Apply the FIPS-specific security properties, if needed
#
include ../${__redhat_fips__}/fips.properties
EOF

# /usr/lib/jvm/java-25-openjdk/conf/security/redhat/crypto-policies.properties
install --mode 644 /dev/stdin "${VENDOR}"/crypto-policies.properties <<'EOF'
#
# Default choice for the crypto-policies setup
#
include true/crypto-policies.properties
EOF

# /usr/lib/jvm/java-25-openjdk/conf/security/redhat/false/fips.properties
install --mode 644 /dev/stdin "${VENDOR}"/false/fips.properties <<'EOF'
# Empty on purpose, for when FIPS is disabled.
EOF

# /usr/lib/jvm/java-25-openjdk/conf/security/redhat/true/fips.properties
install --mode 644 /dev/stdin "${VENDOR}"/true/fips.properties <<'EOF'
#
# Enable the downstream-patch RedHatFIPSFilter code
#
__redhat_fips_filter__=true

#
# FIPS mode Security Providers List
#
security.provider.1=SunPKCS11 ${java.home}/conf/security/redhat/SunPKCS11-FIPS.cfg
security.provider.2=SUN
security.provider.3=SunEC
security.provider.4=SunJSSE
security.provider.5=SunJCE
security.provider.6=SunRsaSign
security.provider.7=XMLDSig
security.provider.8=
#                   ^ empty on purpose, to finish the Providers List

#
# FIPS mode default keystore type
#
keystore.type=pkcs12
EOF

# Make sure java.security exists before appending
test -e "${SECURITY}"/java.security || ( echo "${SECURITY}/java.security not found" && false )
cp -v "${SECURITY}"/java.security "${SECURITY}"/java.security.upstream
cat >> "${SECURITY}"/java.security <<'EOF'

#
# System-wide crypto-policies and FIPS setup
# If you need to use (eg for jlinked image without jmods) the  original one
# backup this, and rename java.security.upstream to java.security
# in case of jlinked image, you can use also --ignore-modified-runtime,
# but it may misbehave later.
#
#
# The following crypto-policies setup automatically detects when the system
# is in FIPS mode and configures OpenJDK accordingly. If OpenJDK needs to
# ignore the system and disable its FIPS setup, just disable the usage of
# the system crypto-policies, by any of the methods described below.
#
# The redhat.crypto-policies system property is a boolean switch that
# controls the usage on a per-run basis. For example, pass
# -Dredhat.crypto-policies=false to disable the system crypto-policies.
#
# This setup consists of the following files in $JAVA_HOME/conf/security:
#
#   'redhat/false/crypto-policies.properties' (policies usage disabled file)
#      Empty file, applied when the boolean switch is passed as false.
#
#   'redhat/true/crypto-policies.properties' (policies usage enabled file)
#      Performs the crypto-policies and FIPS setup, applied when the boolean
#      switch is passed as true.
#
#   'redhat/crypto-policies.properties' (policies usage default file)
#      Determines the default choice by including one of the previous files,
#      applied when the boolean switch is not passed.
#      The system crypto-policies usage is enabled by default:
#        include true/crypto-policies.properties
#
# To enable or disable the usage of the crypto-policies on a per-deployment
# basis, edit the policies usage default file, changing the included file.
# For example, execute the following command to persistently disable the
# crypto-policies:
#   sed -i s/true/false/ $JAVA_HOME/conf/security/redhat/crypto-policies.properties
# Applications can still override this on a per-run basis, for example by
# passing -Dredhat.crypto-policies=true.
#
# To disable the redhat.crypto-policies boolean switch, modify the following
# include directive as follows. Replace ${redhat.crypto-policies} by true to
# force-apply the system crypto-policies:
#   include redhat/true/crypto-policies.properties
# Remove or comment out the include directive to force-disable the setup:
#   #include redhat/${redhat.crypto-policies}/crypto-policies.properties
#
include redhat/${redhat.crypto-policies}/crypto-policies.properties
#       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# WARNING: anything placed after this include directive will apply on top
# of the described setup. Adding properties below this section is strongly
# discouraged, as it poses a risk of overriding the system crypto-policies
# or invalidating the FIPS deployment.
EOF

# Local Variables:
# compile-command: "shellcheck create-redhat-properties-files.bash"
# End:
