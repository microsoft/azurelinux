Summary:        Linux Pluggable Authentication Modules
Name:           pam
Version:        1.3.1
Release:        5%{?dist}
License:        BSD and GPLv2+
URL:            http://www.linux-pam.org/
Source0:        https://github.com/linux-pam/linux-pam/releases/download/v%{version}/Linux-PAM-%{version}.tar.xz
Group:          System Environment/Security
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  cracklib-devel
BuildRequires:  libselinux-devel
Requires:       cracklib
%description
The Linux PAM package contains Pluggable Authentication Modules used to
enable the local system administrator to choose how applications authenticate users.

%package lang
Summary: Additional language files for pam
Group: System Environment/Base
Requires:       %{name} = %{version}-%{release}
%description lang
These are the additional language files of pam.

%package        devel
Summary:        Development files for pam
Group:          System Environment/Base
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains libraries, header files and documentation
for developing applications that use pam.

%prep
%setup -qn Linux-PAM-%{version}
%build

./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --sysconfdir=/etc   \
    --enable-securedir=/usr/lib/security \
    --enable-selinux \
    --docdir=%{_docdir}/%{name}-%{version}

make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot}
chmod -v 4755 %{buildroot}/sbin/unix_chkpwd
install -v -dm755 %{buildroot}/%{_docdir}/%{name}-%{version}
ln -sf pam_unix.so %{buildroot}/usr/lib/security/pam_unix_auth.so
ln -sf pam_unix.so %{buildroot}/usr/lib/security/pam_unix_acct.so
ln -sf pam_unix.so %{buildroot}/usr/lib/security/pam_unix_passwd.so
ln -sf pam_unix.so %{buildroot}/usr/lib/security/pam_unix_session.so
echo 'PATH="/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin"' >> %{buildroot}/etc/environment
find %{buildroot}/%{_libdir} -name '*.la' -delete
find %{buildroot}/usr/lib/ -name '*.la' -delete
%{find_lang} Linux-PAM

%{_fixperms} %{buildroot}/*

%check
install -v -m755 -d /etc/pam.d
cat > /etc/pam.d/other << "EOF"
auth     required       pam_deny.so
account  required       pam_deny.so
password required       pam_deny.so
session  required       pam_deny.so
EOF
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%license COPYING
%{_sysconfdir}/*
/sbin/*
%{_lib}/security/*
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
*   Fri Aug 28 2020 Daniel Burgener <daburgen@microsoft.com> 1.3.1-5
-   Add SELinux support
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
