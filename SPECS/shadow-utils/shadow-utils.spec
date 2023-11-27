Summary:        Programs for handling passwords in a secure way
Name:           shadow-utils
Version:        4.9
Release:        14%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://github.com/shadow-maint/shadow/
Source0:        https://github.com/shadow-maint/shadow/releases/download/v%{version}/shadow-%{version}.tar.xz
Source1:        chage
Source2:        chpasswd
Source3:        login
Source4:        other
Source5:        passwd
Source6:        sshd
Source8:        system-account
Source9:        system-auth
Source10:       system-password
Source11:       system-session
Source12:       useradd-default
Source13:       login-defs
Patch0:         chkname-allowcase.patch
Patch1:         libsubid-pam-link.patch
Patch2:         CVE-2023-29383.patch
BuildRequires:  autoconf
BuildRequires:  audit-devel
BuildRequires:  automake
BuildRequires:  cracklib
BuildRequires:  cracklib-devel
BuildRequires:  docbook-dtd-xml
BuildRequires:  docbook-style-xsl
BuildRequires:  itstool
BuildRequires:  libxcrypt-devel
BuildRequires:  libselinux-devel
BuildRequires:  libsemanage-devel
BuildRequires:  libtool
BuildRequires:  libxslt
BuildRequires:  pam-devel
Requires:       audit-libs
Requires:       cracklib
Requires:       libpwquality
Requires:       libselinux
Requires:       libsemanage
Requires:       pam
Provides:       /sbin/nologin
Provides:       /usr/sbin/groupadd
Provides:       /usr/sbin/groupdel
Provides:       /usr/sbin/nologin
Provides:       /usr/sbin/useradd
Provides:       /usr/sbin/userdel
Provides:       passwd = %{version}-%{release}

%description
The Shadow package contains programs for handling passwords
in a secure way.

%package        subid
Summary:        A library to manage subordinate uid and gid ranges

%description    subid
Utility library that provides a way to manage subid ranges.

%package        subid-devel
Summary:        Libraries and headers for libsubid
Requires:       %{name}-subid = %{version}-%{release}

%description    subid-devel
Libraries and headers for libsubid

%prep
%setup -q -n shadow-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

autoreconf -fiv

sed -i 's/groups$(EXEEXT) //' src/Makefile.in
find man -name Makefile.in -exec sed -i 's/groups\.1 / /' {} \;
sed -i -e 's@#ENCRYPT_METHOD DES@ENCRYPT_METHOD SHA512@' \
    -e 's@%{_var}/spool/mail@%{_var}/mail@' etc/login.defs

sed -i 's@DICTPATH.*@DICTPATH\t/usr/share/cracklib/pw_dict@' \
    etc/login.defs

%build
%configure \
    --sysconfdir=%{_sysconfdir} \
    --with-libpam \
    --with-libcrack \
    --with-group-name-max-length=32 \
    --with-selinux \
    --with-audit \
    --enable-man \
    --with-su=no
%make_build

%install
%make_install
install -vdm 755 %{buildroot}/bin
install -vdm755 %{buildroot}%{_sysconfdir}/default
mv -v %{buildroot}%{_bindir}/passwd %{buildroot}/bin
chmod ug-s %{buildroot}/bin/passwd
install -vm644 %{SOURCE12} %{buildroot}%{_sysconfdir}/default/useradd
install -vm644 %{SOURCE13} %{buildroot}%{_sysconfdir}/login.defs
ln -s useradd %{buildroot}%{_sbindir}/adduser
cp etc/{limits,login.access} %{buildroot}%{_sysconfdir}
for FUNCTION in FAIL_DELAY               \
                FAILLOG_ENAB             \
                LASTLOG_ENAB             \
                MAIL_CHECK_ENAB          \
                OBSCURE_CHECKS_ENAB      \
                PORTTIME_CHECKS_ENAB     \
                QUOTAS_ENAB              \
                CONSOLE MOTD_FILE        \
                FTMP_FILE NOLOGINS_FILE  \
                ENV_HZ PASS_MIN_LEN      \
                SU_WHEEL_ONLY            \
                CRACKLIB_DICTPATH        \
                PASS_CHANGE_TRIES        \
                PASS_ALWAYS_WARN         \
                CHFN_AUTH                \
                ENVIRON_FILE
do
    sed -i "s/^${FUNCTION}/# &/" %{buildroot}%{_sysconfdir}/login.defs
done

install -vm644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE4} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE5} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE6} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE8} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE9} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE10} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE11} %{buildroot}%{_sysconfdir}/pam.d/

for PROGRAM in chfn chgpasswd chsh groupadd groupdel \
               groupmems groupmod newusers useradd userdel usermod
do
    install -v -m644 %{buildroot}%{_sysconfdir}/pam.d/chage %{buildroot}%{_sysconfdir}/pam.d/${PROGRAM}
    sed -i "s/chage/$PROGRAM/" %{buildroot}%{_sysconfdir}/pam.d/${PROGRAM}
done

find %{buildroot} -type f -name "*.la" -delete -print

%find_lang shadow

%check
%make_build check

%post
%{_sbindir}/pwconv
%{_sbindir}/grpconv
chmod 000 %{_sysconfdir}/shadow

%files -f shadow.lang
%defattr(-,root,root)
%license COPYING
%config(noreplace) %{_sysconfdir}/login.defs
%config(noreplace) %{_sysconfdir}/login.access
%config(noreplace) %{_sysconfdir}/default/useradd
%config(noreplace) %{_sysconfdir}/limits
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/*
%attr(4755,root,root) /bin/passwd
%config(noreplace) %{_sysconfdir}/pam.d/*
%attr(0000,root,root) %config(noreplace,missingok) %ghost %{_sysconfdir}/shadow

%files subid
%license COPYING
%{_libdir}/libsubid.so.3*

%files subid-devel
%{_includedir}/shadow/subid.h
%{_libdir}/libsubid.so

%changelog
* Fri Nov 10 2023 Andrew Phelps <anphel@microsoft.com> - 4.9-14
- Switch to link with libxcrypt

* Wed Sep 20 2023 Kanika Nema <kanikanema@microsoft.com> - 4.9-13
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)
- Address CVE-2023-29383

* Wed May 24 2023 Tobias Brick <tobiasb@microsoft.com> - 4.9-12
- Add SETUID bit to passwd binary

* Mon Jul 18 2022 Minghe Ren <mingheren@microsoft.com> - 4.9-11
- Update login-defs, system-auth, passwd to improve security

* Fri Jul 01 2022 Andrew Phelps <anphel@microsoft.com> - 4.9-10
- Remove su binary which is now provided by util-linux
- Update BuildRequires to ensure man pages build

* Mon Apr 18 2022 Minghe Ren <mingheren@microsoft.com> - 4.9-9
- Change /etc/shadow file permission to 000 and make it trackable by shadow-utils

* Fri Mar 25 2022 Rachel Menge <rachelmenge@microsoft.com> - 4.9-8
- Add requires libpwquality

* Fri Mar 04 2022 Andrew Phelps <anphel@microsoft.com> - 4.9-7
- Build with audit-libs
- Add BR for itstool

* Fri Nov 12 2021 Andrew Phelps <anphel@microsoft.com> - 4.9-6
- Add provides to resolve dynamic dependencies

* Mon Oct 11 2021 Chris PeBenito <chpebeni@microsoft.com> - 4.9-5
- Make pam_loginuid use optional for systems that don't have audit.
- License verified.

* Tue Sep 21 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.9-4
- Adding missing BR for "libxslt".
- Removing not built man pages.

* Thu Sep 16 2021 Chris PeBenito <chpebeni@microsoft.com> - 4.9-3
- Update pam.d configuration for SELinux logins.
- Change loginuid to be set only on logins.
- Add missing BuildRequires for xsltproc.

* Fri Sep 10 2021 Thomas Crain <thcrain@microsoft.com> - 4.9-2
- Update system-password PAM config to use pam_pwquality.so instead of removed pam_cracklib.so
- Add license to subid subpackage

* Fri Aug 13 2021 Thomas Crain <thcrain@microsoft.com> - 4.9-1
- Upgrade to latest upstream version and rebase chkname patch
- Add upstream patch to deal with libsubid build failure when linking to pam
- Add %%{_sysconfdir}/login.defs and %{_syconfdir}/default/useradd to sources
-   since they are not auto-generated during packaging
- Create %%{name}-subid and %%{name}-subid-devel subpackages

* Thu Jul 29 2021 Jon Slobodzian <joslobo@microsoft.com> - 4.6-15
- Dash Rolled for Merge from 1.0 branch

* Tue Jun 15 2021 Daniel Burgener <daburgen@microsoft.com> - 4.6-14
- Fix issue with undocumented libselinux and libsemanage requirements

* Wed May 26 2021 Daniel Burgener <daburgen@microsoft.com> - 4.6-13
- Add SELinux support

* Thu May 20 2021 Thomas Crain <thcrain@microsoft.com> - 4.6-12
- Enable usergroups for useradd

* Fri Mar 26 2021 Thomas Crain <thcrain@microsoft.com> 4.6-11
- Merge the following releases from 1.0 to dev branch
- schalam@microsoft.com, 4.6-9: Remove PASS_MAX_DAYS customized value 90 to set default value
- lihl@microsoft.com, 4.6-10: Add sym link to adduser from useradd and create the file for adduser

* Mon Mar 01 2021 Henry Li <lihl@microsoft.com> - 4.6-10
- Add sym link to adduser from useradd and create the file for adduser

* Fri Dec 11 2020 Joe Schmitt <joschmit@microsoft.com> - 4.6-10
- Provide passwd.

* Tue Nov 03 2020 Joe Schmitt <joschmit@microsoft.com> - 4.6-9
- Provide /sbin/nologin.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 4.6-8
- Added %%license line automatically

* Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> - 4.6-7
- Renaming Linux-PAM to pam

* Tue Apr 14 2020 Emre Girgin <mrgirgin@microsoft.com> - 4.6-6
- Consolidate all subpackages as one and rename it to shadow-utils.
- Update the URL.

* Thu Apr 09 2020 Nicolas Ontiveros <niontive@microsoft.com> - 4.6-5
- Remove toybox and only use shadow-tools for requires.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 4.6-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Oct 24 2018 Michelle Wang <michellew@vmware.com> - 4.6-3
- Add su and login into shadow-tool.

* Tue Oct 2 2018 Michelle Wang <michellew@vmware.com> - 4.6-2
- Add conflict toybox for shadow-tools.

* Wed Sep 19 2018 Srinidhi Rao <srinidhir@vmware.com> - 4.6-1
- Upgrading the version to 4.6.

* Mon Jul 30 2018 Tapas Kundu <tkundu@vmware.com> - 4.2.1-16
- Added fix for CVE-2018-7169.

* Fri Apr 20 2018 Alexey Makhalov <amakhalov@vmware.com> - 4.2.1-15
- Move pam.d config file to here for better tracking.
- Add pam_loginuid module as optional in a session.

* Tue Oct 10 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.2.1-14
- Added -tools subpackage.
- Main package requires -tools or toybox.

* Tue Aug 15 2017 Anish Swaminathan <anishs@vmware.com> - 4.2.1-13
- Added fix for CVE-2017-12424, CVE-2016-6252.

* Thu Apr 27 2017 Divya Thaluru <dthaluru@vmware.com> - 4.2.1-12
- Allow '.' in username.

* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> - 4.2.1-11
- BuildRequires Linux-PAM-devel.

* Wed Nov 23 2016 Alexey Makhalov <amakhalov@vmware.com> - 4.2.1-10
- Added -lang subpackage.

* Tue Oct 04 2016 ChangLee <changlee@vmware.com> - 4.2.1-9
- Modified %check.

* Tue Jun 21 2016 Divya Thaluru <dthaluru@vmware.com> - 4.2.1-8
- Added logic to not replace pam.d conf files in upgrade scenario.

* Fri May 27 2016 Divya Thaluru <dthaluru@vmware.com> - 4.2.1-7
- Adding pam_cracklib module as requisite to pam password configuration.

* Wed May 25 2016 Divya Thaluru <dthaluru@vmware.com> - 4.2.1-6
- Modifying pam_systemd module as optional in a session.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.2.1-5
- GA Bump release of all rpms.

* Mon May 2 2016 Xiaolin Li <xiaolinl@vmware.com> - 4.2.1-4
- Enabling pam_systemd module in a session.

* Fri Apr 29 2016 Divya Thaluru <dthaluru@vmware.com> - 4.2.1-3
- Setting password aging limits to 90 days.

* Wed Apr 27 2016 Divya Thaluru <dthaluru@vmware.com> - 4.2.1-3
- Setting password aging limits to 365 days.

* Wed Mar 23 2016 Divya Thaluru <dthaluru@vmware.com> - 4.2.1-2
- Enabling pam_limits module in a session.

* Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com> - 4.2.1-1
- Update version.

* Wed Dec 2 2015 Divya Thaluru <dthaluru@vmware.com> - 4.1.5.1-6
- Fixed PAM Configuration file for passwd.

* Mon Oct 26 2015 Sharath George <sharathg@vmware.com> - 4.1.5.1-5
- Allow mixed case in username.

* Mon Jun 29 2015 Divya Thaluru <dthaluru@vmware.com> - 4.1.5.1-4
- Fixed PAM Configuration file for chpasswd.

* Tue Jun 16 2015 Alexey Makhalov <amakhalov@vmware.com> - 4.1.5.1-3
- Use group id 100(users) by default.

* Wed May 27 2015 Divya Thaluru <dthaluru@vmware.com> - 4.1.5.1-2
- Adding PAM support.

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> - 4.1.5.1-1
- Initial build First version.
