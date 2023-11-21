Summary:        Linux Pluggable Authentication Modules
Name:           pam
Version:        1.5.3
Release:        1%{?dist}
License:        BSD and GPLv2+
URL:            https://github.com/linux-pam/linux-pam
Source0:        https://github.com/linux-pam/linux-pam/releases/download/v%{version}/Linux-PAM-%{version}.tar.xz
Group:          System Environment/Security
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  cracklib-devel
BuildRequires:  libxcrypt-devel
BuildRequires:  libselinux-devel
BuildRequires:  audit-devel
Requires:       audit-libs
Recommends:     cracklib-dicts

%description
The Linux PAM package contains Pluggable Authentication Modules used to
enable the local system administrator to choose how applications authenticate users.

%package        lang
Summary:        Additional language files for pam
Group:          System Environment/Base
Requires:       %{name} = %{version}-%{release}

%description    lang
These are the additional language files of pam.

%package        devel
Summary:        Development files for pam
Group:          System Environment/Base
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains libraries, header files and documentation
for developing applications that use pam.

%prep
%autosetup -n Linux-PAM-%{version}

%build
./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --sysconfdir=/etc   \
    --enable-securedir=/usr/lib/security \
    --enable-selinux \
    --docdir=%{_docdir}/%{name}-%{version} \
    --disable-db
%make_build

%install
%make_install

chmod -v 4755 %{buildroot}/sbin/unix_chkpwd
install -v -dm755 %{buildroot}/%{_docdir}/%{name}-%{version}
ln -sf pam_unix.so %{buildroot}%{_libdir}/security/pam_unix_auth.so
ln -sf pam_unix.so %{buildroot}%{_libdir}/security/pam_unix_acct.so
ln -sf pam_unix.so %{buildroot}%{_libdir}/security/pam_unix_passwd.so
ln -sf pam_unix.so %{buildroot}%{_libdir}/security/pam_unix_session.so
echo 'PATH="/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin"' >> %{buildroot}/etc/environment
find %{buildroot} -name "*.la" -delete -print
%{find_lang} Linux-PAM

%{_fixperms} %{buildroot}/*

%check
install -v -m755 -d %{_sysconfdir}/pam.d
cat > %{_sysconfdir}/pam.d/other << "EOF"
auth     required       pam_deny.so
account  required       pam_deny.so
password required       pam_deny.so
session  required       pam_deny.so
EOF
%make_build check

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license COPYING
%{_sysconfdir}/*
/sbin/*
%{_libdir}/security/*
%{_libdir}/systemd/system/pam_namespace.service
%{_libdir}/*.so*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files lang -f Linux-PAM.lang
%defattr(-,root,root)

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_mandir}/man3/*
%{_docdir}/%{name}-%{version}/*

%changelog
* Tue Nov 21 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.5.3-1
- Auto-upgrade to 1.5.3 - Azure Linux 3.0 - package upgrades

* Fri Nov 10 2023 Andrew Phelps <anphel@microsoft.com> - 1.5.1-6
- Switch to link with libxcrypt

* Tue Mar 22 2022 Andrew Phelps <anphel@microsoft.com> - 1.5.1-5
- Require audit-libs

* Mon Mar 14 2022 Andrew Phelps <anphel@microsoft.com> - 1.5.1-4
- Add Recommends for audit-libs and cracklib-dicts to resolve circular dependency and boot issue

* Fri Mar 04 2022 Andrew Phelps <anphel@microsoft.com> - 1.5.1-3
- Build with audit support

* Tue Oct 19 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.5.1-2
- Remove libdb dependency

* Fri Aug 13 2021 Thomas Crain <thcrain@microsoft.com> - 1.5.1-1
- Upgrade to latest upstream version

* Tue Feb 16 2021 Daniel Burgener <daburgen@microsoft.com> 1.3.1-6
- Add SELinux support (JOSLOBO 7/26/21 bumped dash version to resolve merge conflict)

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 1.3.1-5
- Replace incorrect %%{_lib} usage with %%{_libdir}

*   Fri Jun 12 2020 Chris Co <chrco@microsoft.com> 1.3.1-4
-   Set default PATH in /etc/environment
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.3.1-3
-   Added %%license line automatically
*   Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> 1.3.1-2
-   Renaming Linux-PAM to pam
*   Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> 1.3.1-1
-   Update to 1.3.1. Fix URL. Fix Source0 URL. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.3.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.3.0-1
-   Version update.
*   Fri Feb 10 2017 Xiaolin Li <xiaolinl@vmware.com> 1.2.1-5
-   Added pam_unix_auth.so, pam_unix_acct.so, pam_unix_passwd.so,
-   and pam_unix_session.so.
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.2.1-4
-   Added devel subpackage.
*   Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com> 1.2.1-3
-   Packaging pam cracklib module
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.1-2
-   GA - Bump release of all rpms
*   Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 1.2.1-1
-   Updated to version 1.2.1
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.1.8-2
-   Update according to UsrMove.
*   Thu Oct 09 2014 Divya Thaluru <dthaluru@vmware.com> 1.1.8-1
-   Initial build.  First version
