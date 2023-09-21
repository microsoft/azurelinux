%global openssh_ver 8.9p1
%global pam_ssh_agent_ver 0.10.3
Summary:        Free version of the SSH connectivity tools
Name:           openssh
Version:        %{openssh_ver}
Release:        2%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://www.openssh.com/
Source0:        https://ftp.usa.openbsd.org/pub/OpenBSD/OpenSSH/portable/%{name}-%{openssh_ver}.tar.gz
Source1:        sshd.service
Source2:        sshd-keygen.service
Source3:        https://prdownloads.sourceforge.net/pamsshagentauth/pam_ssh_agent_auth/pam_ssh_agent_auth-%{pam_ssh_agent_ver}.tar.bz2
Source4:        pam_ssh_agent-rmheaders
# Nopatches section
# Community agreed to not patch this
Patch100:       CVE-2007-2768.nopatch
# --- pam_ssh-agent ---
# make it build reusing the openssh sources
Patch300:       pam_ssh_agent_auth-0.9.3-build.patch
# check return value of seteuid()
# https://sourceforge.net/p/pamsshagentauth/bugs/23/
Patch301:       pam_ssh_agent_auth-0.10.3-seteuid.patch
# explicitly make pam callbacks visible
Patch302:       pam_ssh_agent_auth-0.9.2-visibility.patch
# update to current version of agent structure
Patch305:       pam_ssh_agent_auth-0.9.3-agent_structure.patch
# remove prefixes to be able to build against current openssh library
Patch306:       pam_ssh_agent_auth-0.10.2-compat.patch
# Fix NULL dereference from getpwuid() return value
# https://sourceforge.net/p/pamsshagentauth/bugs/22/
Patch307:       pam_ssh_agent_auth-0.10.2-dereference.patch
Patch308:       CVE-2023-38408.patch
BuildRequires:  audit-devel
BuildRequires:  autoconf
BuildRequires:  e2fsprogs-devel
BuildRequires:  groff
BuildRequires:  kernel-headers
BuildRequires:  krb5-devel
BuildRequires:  libselinux-devel
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  pam-devel
BuildRequires:  systemd
%if %{with_check}
BuildRequires:  shadow-utils
BuildRequires:  sudo
%endif
Requires:       audit-libs
Requires:       openssh-clients = %{openssh_ver}-%{release}
Requires:       openssh-server = %{openssh_ver}-%{release}

%description
The OpenSSH package contains ssh clients and the sshd daemon. This is
useful for encrypting authentication and subsequent traffic over a
network. The ssh and scp commands are secure implementions of telnet
and rcp respectively.

%package clients
Summary:        openssh client applications.
Requires:       openssl

%description clients
This provides the ssh client utilities.

%package server
Summary:        openssh server applications
Requires:       ncurses-term
Requires:       openssh-clients = %{openssh_ver}-%{release}
Requires:       pam
Requires:       shadow-utils
Requires(post): /bin/chown
Requires(pre):  %{_sbindir}/groupadd
Requires(pre):  %{_sbindir}/useradd

%description server
This provides the ssh server daemons, utilities, configuration and service files.

%package -n pam_ssh_agent_auth
Summary:        PAM module for authentication with ssh-agent
Version:        %{pam_ssh_agent_ver}
Release:        11%{?dist}

%description -n pam_ssh_agent_auth
This package contains a PAM module which can be used to authenticate
users using ssh keys stored in a ssh-agent. Through the use of the
forwarding of ssh-agent connection it also allows to authenticate with
remote ssh-agent instance.

The module is most useful for su and sudo service stacks.

%prep
%setup -q -a 3

pushd pam_ssh_agent_auth-%{pam_ssh_agent_ver}
%patch300 -p2 -b .psaa-build
%patch301 -p2 -b .psaa-seteuid
%patch302 -p2 -b .psaa-visibility
%patch306 -p2 -b .psaa-compat
%patch305 -p2 -b .psaa-agent
%patch307 -p2 -b .psaa-deref
# Remove duplicate headers and library files
rm -f $(cat %{SOURCE4})
autoreconf
popd
%patch308 -p2 -b .cve-2023-38408

%build
# The -fvisibility=hidden is needed for clean build of the pam_ssh_agent_auth.
export CFLAGS="$CFLAGS -fvisibility=hidden -fpic"
SAVE_LDFLAGS="$LDFLAGS"
export LDFLAGS="$LDFLAGS -pie -z relro -z now"
%configure \
    --sysconfdir=%{_sysconfdir}/ssh \
    --datadir=%{_datadir}/sshd \
    --with-md5-passwords \
    --with-privsep-path=%{_sharedstatedir}/sshd \
    --with-pam \
    --with-pie=no \
    --with-selinux \
    --with-audit=linux \
    --with-maintype=man \
    --without-hardening `# The hardening flags are configured by system` \
    --enable-strip=no \
    --with-kerberos5=%{_prefix}
%make_build

pushd pam_ssh_agent_auth-%{pam_ssh_agent_ver}
export LDFLAGS="$SAVE_LDFLAGS"
%configure  --with-selinux \
            --libexecdir=/%{_libdir}/security \
            --with-mantype=man \
            --without-openssl-header-check # The check is broken
%make_build
popd

%install
%make_install
install -vdm755 %{buildroot}%{_sharedstatedir}/sshd

sed -i 's/#UsePAM no/UsePAM yes/' %{buildroot}%{_sysconfdir}/ssh/sshd_config
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' %{buildroot}%{_sysconfdir}/ssh/sshd_config
sed -i 's/#PrintMotd yes/PrintMotd no/' %{buildroot}%{_sysconfdir}/ssh/sshd_config
sed -i 's/#PermitUserEnvironment no/PermitUserEnvironment no/' %{buildroot}%{_sysconfdir}/ssh/sshd_config
sed -i 's/#ClientAliveInterval 0/ClientAliveInterval 120/' %{buildroot}%{_sysconfdir}/ssh/sshd_config
sed -i 's/#ClientAliveCountMax 0/ClientAliveCountMax 0/' %{buildroot}%{_sysconfdir}/ssh/sshd_config

echo "" >> %{buildroot}%{_sysconfdir}/ssh/sshd_config
cat << EOF >> %{buildroot}%{_sysconfdir}/ssh/sshd_config
# Ensure SSH LoginGraceTime is set to one minute or less
LoginGraceTime 60
EOF

sed -i 's/# no default banner path/# default banner path/g' %{buildroot}%{_sysconfdir}/ssh/sshd_config
sed -i 's|#Banner none|Banner /etc/issue.net|' %{buildroot}%{_sysconfdir}/ssh/sshd_config

# Configure to use strong MACs
echo "MACs hmac-sha2-512,hmac-sha2-256" >> %{buildroot}%{_sysconfdir}/ssh/sshd_config
echo "MACs hmac-sha2-512,hmac-sha2-256" >> %{buildroot}%{_sysconfdir}/ssh/ssh_config
# Configure to use strong encryption ciphers
echo "Ciphers aes256-ctr,aes192-ctr,aes128-ctr" >> %{buildroot}%{_sysconfdir}/ssh/sshd_config
echo "Ciphers aes256-ctr,aes192-ctr,aes128-ctr" >> %{buildroot}%{_sysconfdir}/ssh/ssh_config

install -D -m644 %{SOURCE1} %{buildroot}/lib/systemd/system/sshd.service
install -D -m644 %{SOURCE2} %{buildroot}/lib/systemd/system/sshd-keygen.service
install -m755 contrib/ssh-copy-id %{buildroot}/%{_bindir}/
install -m644 contrib/ssh-copy-id.1 %{buildroot}/%{_mandir}/man1/

%{_fixperms} %{buildroot}/*

pushd pam_ssh_agent_auth-%{pam_ssh_agent_ver}
%make_install
popd

%check
if ! getent passwd sshd >/dev/null; then
   useradd sshd
fi
if [ ! -d %{_sharedstatedir}/sshd ]; then
   mkdir %{_sharedstatedir}/sshd
   chmod 0755 %{_sharedstatedir}/sshd
fi
cp %{buildroot}%{_bindir}/scp %{_bindir}
chmod g+w . -R
useradd test -G root -m
sudo -u test -s /bin/bash -c "PATH=$PATH TEST_SSH_UNSAFE_PERMISSIONS=1 make tests"

%pre server
getent group sshd >/dev/null || groupadd --system sshd
getent passwd sshd >/dev/null || useradd --system --comment 'Privilege Separated SSH' --home-dir %{_sharedstatedir}/sshd --gid sshd --shell /bin/false sshd

%preun server
%systemd_preun sshd.service sshd-keygen.service

%post server
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
    chown -v root:sys %{_sharedstatedir}/sshd
fi
%systemd_post sshd.service sshd-keygen.service

%postun server
/sbin/ldconfig
%systemd_postun_with_restart sshd.service sshd-keygen.service
if [ $1 -eq 0 ] ; then
    if getent passwd sshd >/dev/null; then
        userdel sshd
    fi
    if getent group sshd >/dev/null; then
        groupdel sshd
    fi
fi

%files
%license LICENCE

%files -n pam_ssh_agent_auth
%license pam_ssh_agent_auth-%{pam_ssh_agent_ver}/OPENSSH_LICENSE
%attr(0755,root,root) %{_libdir}/security/pam_ssh_agent_auth.so
%attr(0644,root,root) %{_mandir}/man8/pam_ssh_agent_auth.8*

%files server
%defattr(-,root,root)
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/sshd_config
%attr(700,root,sys) %{_sharedstatedir}/sshd
/lib/systemd/system/sshd-keygen.service
/lib/systemd/system/sshd.service
%{_sbindir}/sshd
%{_libexecdir}/sftp-server
%{_mandir}/man5/sshd_config.5.gz
%{_mandir}/man8/sshd.8.gz
%{_mandir}/man5/moduli.5.gz
%{_mandir}/man8/sftp-server.8.gz

%files clients
%attr(0755,root,root) %dir %{_sysconfdir}/ssh
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/moduli
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/ssh_config
%{_bindir}/ssh
%{_bindir}/scp
%{_bindir}/sftp
%{_bindir}/ssh-keygen
%{_bindir}/ssh-keyscan
%{_bindir}/ssh-add
%{_bindir}/ssh-agent
%{_bindir}/ssh-copy-id
%{_libexecdir}/ssh-keysign
%{_libexecdir}/ssh-pkcs11-helper
%{_libexecdir}/ssh-sk-helper
%{_mandir}/man1/scp.1.gz
%{_mandir}/man1/ssh-agent.1.gz
%{_mandir}/man1/ssh-keygen.1.gz
%{_mandir}/man1/ssh-keyscan.1.gz
%{_mandir}/man5/ssh_config.5.gz
%{_mandir}/man1/ssh-add.1.gz
%{_mandir}/man1/ssh.1.gz
%{_mandir}/man1/ssh-copy-id.1.gz
%{_mandir}/man1/sftp.1.gz
%{_mandir}/man8/ssh-keysign.8.gz
%{_mandir}/man8/ssh-pkcs11-helper.8.gz
%{_mandir}/man8/ssh-sk-helper.8.gz

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 8.9p1-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Jul 27 2023 Riken Maharjan <rmaharjan@microsoft.com> - 8.9p1-1
- Fix CVE-2023-38408
- Update to 8.9p1 so that the patch can be applied.

* Tue Jul 26 2022 Minghe Ren <mingheren@microsoft.com> - 8.8p1-7
- Update sshd_config to imporve SSH security

* Fri Apr 22 2022 Chris Co <chrco@microsoft.com> - 8.8p1-6
- Use strong MACs for ssh and sshd
- Use strong encryption ciphers for ssh and sshd

* Mon Apr 11 2022 Andy Caldwell <andycaldwell@microsoft.com> - 8.8p1-5
- Remove socket-triggering for SSHd due to conflicts with non-triggered service and potential DoS vector

* Fri Mar 04 2022 Andrew Phelps <anphel@microsoft.com> - 8.8p1-4
- Build with audit support

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.8p1-3
- Removing the explicit %%clean stage.

* Tue Oct 19 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.8p1-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Oct 6 2021 Rachel Menge <rachelmenge@microsoft.com> 8.8p1-1
- Update to 8.8p1 to patch CVE-2021-41617

* Wed Sep 29 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.5p1-4
- Adding the 'pam_ssh_agent_auth' subpackage using Fedora 32 spec (license: MIT) as guidance.

* Wed Mar 24 2021 Daniel Burgener <daburgen@microsoft.com> 8.5p1-3
- Add SELinux support

* Fri Mar 12 2021 Henry Beberman <henry.beberman@microsoft.com> - 8.5p1-2
- Update default sshd_config to align more closely with other cloud images

* Thu Mar 11 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.5p1-1
- Updating to 8.5p1 to patch CVE-2021-28041.
- Added "TEST_SSH_UNSAFE_PERMISSIONS=1" to enable running more tests.
- Removing patch for CVE-2019-16905, since it's already part of this version.
- Removing nopatch for CVE-2020-14145 and CVE-2020-15778, since the fixes are included in this version.
- Removing regressions test fixes - already part of this version.

* Mon Dec 28 2020 Thomas Crain <thcrain@microsoft.com> - 8.0p1-13
- Add BRs for check section
- Add patch fixing cert-hostkey and cert-userkey regression tests

* Tue Nov 17 2020 Nicolas Guibourge <nicolasg@microsoft.com> - 8.0p1-12
- Nopatching CVE-2020-15778.

* Tue Nov 03 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.0p1-11
- Nopatching CVE-2020-14145.

* Fri Oct 30 2020 Nicolas Ontiveros <niontive@microsoft.com> - 8.0p1-10
- Add no patch for CVE-2007-2768

* Mon Oct 19 2020 Andrew Phelps <anphel@microsoft.com> - 8.0p1-9
- Add patch for CVE-2019-16905

* Wed Sep 02 2020 Jim Perrin <jim.perrin@microsoft.com> - 8.0p1-8
- Add wants=sshd-keygen.service to sshd.service for easier service starting

* Thu Jun 04 2020 Chris Co <chrco@microsoft.com> - 8.0p1-7
- Use default MaxAuthTries value of 6

* Tue May 26 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.0p1-6
- Adding the "%%license" macro.

* Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> - 8.0p1-5
- Renaming Linux-PAM to pam

* Mon Apr 27 2020 Emre Girgin <mrgirgin@microsoft.com> - 8.0p1-4
- Rename shadow to shadow-utils.

* Mon Apr 27 2020 Emre Girgin <mrgirgin@microsoft.com> - 8.0p1-3
- Rename ncurses-terminfo to ncurses-term.

* Fri Apr 24 2020 Nick Samson <nisamson@microsoft.com> - 8.0p1-2
- Updated Source0, Source1. blfs-systemd-units updated to latest recommended version (20191026).

* Thu Mar 12 2020 Paul Monson <paulmon@microsoft.com> - 8.0p1-1
- Update to version 8.0p1. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 7.8p1-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Feb 14 2019 Ankit Jain <ankitja@vmware.comm> - 7.8p1-3
- Fix CVE-2018-20685.

* Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> - 7.8p1-2
- Added BuildRequires groff
- Use %configure

* Tue Sep 11 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> - 7.8p1-1
- Update version

* Tue Nov 28 2017 Xiaolin Li <xiaolinl@vmware.comm> - 7.5p1-11
- Fix CVE-2017-15906.

* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 7.5p1-10
- Fix: openssh-server requires(pre) shadow tools

* Tue Nov 14 2017 Anish Swaminathan <anishs@vmware.com> - 7.5p1-9
- Add ciphers aes128-gcm, aes256-gcm and kex dh14/16/18 in fips mode

* Tue Oct 10 2017 Alexey Makhalov <amakhalov@vmware.com> - 7.5p1-8
- No direct toybox dependency, shadow depends on toybox

* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> - 7.5p1-7
- Requires shadow or toybox

* Thu Sep 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 7.5p1-6
- sshd config: revert MaxSessions to original value

* Thu Aug 31 2017 Alexey Makhalov <amakhalov@vmware.com> - 7.5p1-5
- sshd config hardening based on lynis recommendations

* Thu Aug 10 2017 Chang Lee <changlee@vmware.com> - 7.5p1-4
- Fixed %check

* Mon Jul 24 2017 Dheeraj Shetty <dheerajs@vmware.com> - 7.5p1-3
- Seperate the service file from the spec file

* Wed May 3  2017 Bo Gan <ganb@vmware.com> - 7.5p1-2
- Fixed openssh-server dependency on coreutils

* Tue Mar 28 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 7.5p1-1
- Update version

* Thu Feb 09 2017 Anish Swaminathan <anishs@vmware.com> - 7.4p1-3
- Add patch to configure openssh FIPS mode

* Thu Feb 02 2017 Anish Swaminathan <anishs@vmware.com> - 7.4p1-2
- Add patch to support FIPS mode

* Fri Jan 06 2017 Xiaolin Li <xiaolinl@vmware.com> - 7.4p1-1
- Updated to version 7.4p1.

* Wed Dec 14 2016 Xiaolin Li <xiaolinl@vmware.com> - 7.1p2-10
- BuildRequires Linux-PAM-devel

* Mon Dec 12 2016 Anish Swaminathan <anishs@vmware.com> - 7.1p2-9
- Add patch to fix CVE-2016-8858

* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> - 7.1p2-8
- openssh-devel requires ncurses-terminfo to provide extra terms
    for the clients

* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> - 7.1p2-7
- Required krb5-devel.

* Thu Nov 03 2016 Sharath George <sharathg@vmware.com> - 7.1p2-6
- Split openssh into client and server rpms.

* Wed Oct 05 2016 ChangLee <changlee@vmware.com> - 7.1p2-5
- Modified %check

* Thu Sep 15 2016 Anish Swaminathan <anishs@vmware.com> - 7.1p2-4
- Add patch to fix CVE-2016-6515

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 7.1p2-3
- GA - Bump release of all rpms

* Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> - 7.1p2-2
- Edit scriptlets.

* Thu Mar 17 2016 Xiaolin Li <xiaolinl@vmware.com> - 7.1p2-1
- Updated to version 7.1p2

* Fri Feb 05 2016 Anish Swaminathan <anishs@vmware.com> - 6.6p1-6
- Add pre install scripts in the rpm

* Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com> - 6.6p1-5
- Change config file attributes.

* Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com> - 6.6p1-4
- Add systemd to Requires and BuildRequires.
- Use systemctl to enable/disable service.

* Fri Jul 17 2015 Divya Thaluru <dthaluru@vmware.com> - 6.6p1-3
- Enabling ssh-keygen service by default and fixed service file to execute only once.

* Tue May 19 2015 Sharath George <sharathg@vmware.com> - 6.6p1-2
- Bulding ssh server with kerberos 5.

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> - 6.6p1-1
- Initial build. First version
