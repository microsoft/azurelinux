Summary:        Sudo
Name:           sudo
Version:        1.9.14p3
Release:        2%{?dist}
License:        ISC
URL:            https://www.sudo.ws/
Group:          System Environment/Security
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://www.sudo.ws/sudo/dist/%{name}-%{version}.tar.gz
Patch0:         sudo-ldap-netgroup-query.patch
BuildRequires:  audit-devel
BuildRequires:  man-db
BuildRequires:  openssl-devel
BuildRequires:  openssl-libs
BuildRequires:  pam-devel
BuildRequires:  sed
BuildRequires:  zlib-devel
BuildRequires:  openldap-devel
Requires:       audit-libs
Requires:       openssl-libs
Requires:       pam
Requires:       shadow-utils
Requires:       zlib

%description
The Sudo package allows a system administrator to give certain users (or groups of users)
the ability to run some (or all) commands as root or another user while logging the commands and arguments.

%prep
%setup -q

%build
./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libexecdir=%{_libdir} \
    --docdir=%{_docdir}/%{name}-%{version} \
    --with-env-editor \
    --with-pam \
    --with-ldap \
    --with-linux-audit \
    --enable-zlib=system \
    --with-passprompt="[sudo] password for %p: "

make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot}
install -v -dm755 %{buildroot}/%{_docdir}/%{name}-%{version}
find %{buildroot}/%{_libdir} -name '*.la' -delete
find %{buildroot}/%{_libdir} -name '*.so~' -delete
# Add default user to sudoers group BEFORE the @includedir
sed -i -E '/## Read drop-in files.+/i %wheel ALL=(ALL) ALL\n%sudo  ALL=(ALL) ALL' %{buildroot}/etc/sudoers
install -vdm755 %{buildroot}/etc/pam.d
cat > %{buildroot}/etc/pam.d/sudo << EOF
#%%PAM-1.0
auth       include      system-auth
account    include      system-account
password   include      system-password
session    include      system-session
session    required     pam_env.so
EOF
mkdir -p %{buildroot}%{_libdir}/tmpfiles.d
touch %{buildroot}%{_libdir}/tmpfiles.d/sudo.conf
%find_lang %{name}
%{_fixperms} %{buildroot}/*

%check
make %{?_smp_mflags} check

%post
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
  getent group wheel > /dev/null || groupadd wheel
fi

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%license LICENSE.md
%attr(0440,root,root) %config(noreplace) %{_sysconfdir}/sudoers
%attr(0750,root,root) %dir %{_sysconfdir}/sudoers.d/
%config(noreplace) %{_sysconfdir}/pam.d/sudo
%config(noreplace) %{_sysconfdir}/sudo_logsrvd.conf
%config(noreplace) %{_sysconfdir}/sudo.conf
%{_bindir}/*
%{_includedir}/*
%{_libdir}/sudo/*.so
%{_libdir}/sudo/*.so.*
%{_sbindir}/*
%{_datarootdir}/locale/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_docdir}/%{name}-%{version}/*
%attr(0644,root,root) %{_libdir}/tmpfiles.d/sudo.conf
%exclude  /etc/sudoers.dist

%changelog
* Tue Dec 19  2023 Andy Zaugg <azaugg@linkedin.com> - 1.9.14p3-2
- Add patch to bug fix support for NETGROUP_QUERY

* Fri Aug 25 2023 Andy Zaugg <azaugg@linkedin.com> - 1.9.14p3-1
- Bump version to 1.9.14p3

* Mon May 08 2023 Andy Zaugg <azaugg@linkedin.com> - 1.9.13p3-2
- Add config option to sudo build to allow configuration of sudo via LDAP.

* Thu Mar 16 2023 Thien Trung Vuong <tvuong@microsoft.com> - 1.9.13p3-1
- Upgrade to 1.9.13p3 to fix CVE-2023-27320

* Wed Feb 08 2023 Rachel Menge <rachelmenge@microsoft.com> - 1.9.12p2-1
- Upgrade to 1.9.12p2 for CVE-2023-22809

* Thu Nov 10 2022 Ahmed Badawi <ahmedbadawi@microsoft.com> - 1.9.12p1-1
- Upgrade sudo to version 1.9.12p1 to fix CVE-2022-43995.

* Tue Mar 08 2022 Jon Slobodzian <joslobo@microsoft.com> - 1.9.10
- Upgrade to Latest Stable sudo version for CBL-Mariner 2.0

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.9.5p2-3
- Removing the explicit %%clean stage.

* Mon Feb 22 2021 Mateusz Malisz <mamalisz@microsoft.com> 1.9.5p2-2
- Move sudo/wheel groups before @includedir to not override user's settings.

* Tue Jan 26 2021 Mateusz Malisz <mamalisz@microsoft.com> 1.9.5p2-1
- Update to version 1.9.5.p2 to fix CVE-2021-3156.
- Change the password prompt to include ": " at the end.
- Unconditionally add wheel/sudo groups.

* Fri Jan 15 2021 Mateusz Malisz <mamalisz@microsoft.com> 1.9.5p1-1
- Update to version 1.9.5.p1 to fix CVE-2021-23240.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.8.31p1-4
- Added %%license line automatically

* Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> 1.8.31p1-3
- Renaming Linux-PAM to pam

* Fri Apr 17 2020 Emre Girgin <mrgirgin@microsoft.com> 1.8.31p1-2
- Rename shadow to shadow-utils.

* Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> 1.8.31p1-1
- Update to 1.8.31p1. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.8.23-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Sep 11 2018 Keerthana K <keerthanak@vmware.com> 1.8.23-1
- Update to version 1.8.23.

* Thu Mar 01 2018 Anish Swaminathan <anishs@vmware.com> 1.8.20p2-5
- Move includedir sudoers.d to end of sudoers file

* Tue Oct 10 2017 Alexey Makhalov <amakhalov@vmware.com> 1.8.20p2-4
- No direct toybox dependency, shadow depends on toybox

* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.8.20p2-3
- Requires shadow or toybox

* Fri Jul 07 2017 Chang Lee <changlee@vmware.com> 1.8.20p2-2
- Including /usr/lib/tmpfiles.d/sudo.conf from %files

* Thu Jun 15 2017 Kumar Kaushik <kaushikk@vmware.com> 1.8.20p2-1
- Udating version to 1.8.20p2, fixing CVE-2017-1000367 and CVE-2017-1000368

* Wed Apr 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.8.19p2-1
- Update to version 1.8.19p2

* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.8.18p1-3
- BuildRequires Linux-PAM-devel

* Thu Oct 20 2016 Alexey Makhalov <amakhalov@vmware.com> 1.8.18p1-2
- Remove --with-pam-login to use /etc/pam.d/sudo for `sudo -i`
- Fix groupadd wheel warning during the %post action

* Tue Oct 18 2016 Alexey Makhalov <amakhalov@vmware.com> 1.8.18p1-1
- Update to 1.8.18p1

* Tue Oct 04 2016 ChangLee <changlee@vmware.com> 1.8.15-4
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.15-3
- GA - Bump release of all rpms

* Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.15-2
- Fix for upgrade issues

* Wed Jan 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.15-1
- Update to 1.8.15-1.

* Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 1.8.11p1-5
- Edit post script.

* Mon Jun 22 2015 Divya Thaluru <dthaluru@vmware.com> 1.8.11p1-4
- Fixing permissions on /etc/sudoers file

* Fri May 29 2015 Divya Thaluru <dthaluru@vmware.com> 1.8.11p1-3
- Adding sudo configuration and PAM config file

* Wed May 27 2015 Divya Thaluru <dthaluru@vmware.com> 1.8.11p1-2
- Adding PAM support

* Thu Oct 09 2014 Divya Thaluru <dthaluru@vmware.com> 1.8.11p1-1
- Initial build.  First version
