# Don't depend on bash by default
%define __requires_exclude ^/(bin|usr/bin).*/(ba)?sh$
Summary:        The Kerberos newtork authentication system
Name:           krb5
Version:        1.18.4
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://web.mit.edu/kerberos/
Source0:        https://web.mit.edu/kerberos/dist/%{name}/1.18/%{name}-%{version}.tar.gz
Patch0:         CVE-2021-37750.patch
Patch1:         CVE-2022-42898.patch
BuildRequires:  e2fsprogs-devel
BuildRequires:  openssl-devel
Requires:       e2fsprogs-libs
Requires:       openssl
Provides:       pkgconfig(mit-krb5)
Provides:       pkgconfig(mit-krb5-gssapi)
%if %{with_check}
BuildRequires:  iana-etc
%endif

%description
Kerberos V5 is a trusted-third-party network authentication system,
which can improve your network's security by eliminating the insecure
practice of clear text passwords.

%package devel
Summary:        Libraries and header files for krb5
Requires:       %{name} = %{version}-%{release}

%description devel
Static libraries and header files for the support library for krb5

%package lang
Summary:        Additional language files for krb5
Group:          System Environment/Security
Requires:       %{name} = %{version}-%{release}

%description lang
These are the additional language files of krb5.

%prep
%autosetup -p1

%build
cd src &&
sed -e 's@\^u}@^u cols 300}@' \
    -i tests/dejagnu/config/default.exp &&
CPPFLAGS="-D_GNU_SOURCE %{getenv:CPPFLAGS}" \
autoconf &&
./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --sysconfdir=%{_sysconfdir} \
        --localstatedir=%{_sharedstatedir} \
        --with-system-et         \
        --with-system-ss         \
        --with-system-verto=no   \
        --enable-dns-for-realm   \
        --enable-pkinit          \
        --enable-shared          \
        --without-tcl
make %{?_smp_mflags}

%install
cd src
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot}
find %{buildroot} -type f -name "*.la" -delete -print
for LIBRARY in gssapi_krb5 gssrpc k5crypto kadm5clnt kadm5srv \
               kdb5 krad krb5 krb5support verto ; do
    chmod -v 755 %{buildroot}/%{_libdir}/lib$LIBRARY.so
done

ln -v -sf %{buildroot}/%{_libdir}/libkrb5.so.3.3        %{_lib}/libkrb5.so
ln -v -sf %{buildroot}/%{_libdir}/libk5crypto.so.3.1    %{_lib}/libk5crypto.so
ln -v -sf %{buildroot}/%{_libdir}/libkrb5support.so.0.1 %{_lib}/libkrb5support.so

mv -v %{buildroot}/%{_bindir}/ksu /bin
chmod -v 755 /bin/ksu

install -v -dm755 %{buildroot}/%{_docdir}/%{name}-%{version}

unset LIBRARY
%{_fixperms} %{buildroot}/*

%check
# krb5 tests require hostname resolve
echo "127.0.0.1 $HOSTNAME" >> %{_sysconfdir}/hosts
cd src
make check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%license doc/copyright.rst
%{_bindir}/*
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/krb5/plugins/*
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%{_datarootdir}/man/man5/.k5identity.5.gz
%{_datarootdir}/man/man5/.k5login.5.gz

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_datarootdir}/examples/*
%{_docdir}/*

%files lang
%defattr(-,root,root)
%{_datarootdir}/locale/*

%changelog
* Fri Jan 06 2023 Aadhar Agarwal <aadagarwal@microsoft.com> - 1.18.4-3
- Add patch to fix CVE-2022-42898

* Tue Oct 26 2021 Mateusz Malisz <mamalisz@microsoft.com> - 1.18.4-2
- Remove dependency on sh/bash.

* Tue Oct 19 2021 Neha Agarwal <nehaagarwal@microsoft.com> - 1.18.4-1
- Update version to fix CVE-2019-14844, CVE-2020-28196, CVE-2021-36222
- Add patch to fix CVE-2021-37750

* Mon Oct 19 2020 Andrew Phelps <anphel@microsoft.com> - 1.17-4
- Fix check tests by adding iana-etc which supplies required /etc/services file

* Fri Jul 31 2020 Leandro Pereira <leperei@microsoft.com> - 1.17-3
- Don't stomp on CPPFLAGS

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.17-2
- Added %%license line automatically

*   Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> 1.17-1
-   Update to 1.17. Fix Source0 URL. License verified.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.16.1-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Fri Sep 14 2018 Ankit Jain <ankitja@vmware.com> 1.16.1-1
-   Update to version 1.16.1

*   Wed Dec 13 2017 Xiaolin Li <xiaolinl@vmware.com> 1.16-1
-   Update to version 1.16 to address CVE-2017-15088

*   Thu Sep 28 2017 Xiaolin Li <xiaolinl@vmware.com> 1.15.2-1
-   Update to version 1.15.2

*   Mon Jul 10 2017 Alexey Makhalov <amakhalov@vmware.com> 1.15.1-2
-   Fix make check: add /etc/hosts entry, disable parallel check

*   Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 1.15.1-1
-   Updated to version 1.51.1

*   Wed Nov 23 2016 Alexey Makhalov <amakhalov@vmware.com> 1.14-6
-   Added -lang and -devel subpackages

*   Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 1.14-5
-   Use e2fsprogs-libs as runtime deps

*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.14-4
-   GA - Bump release of all rpms

*   Mon Mar 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com>  1.14-3
-   Add patch to never unload gssapi mechanisms

*   Fri Mar 18 2016 Anish Swaminathan <anishs@vmware.com>  1.14-2
-   Add patch for skipping unnecessary mech calls in gss_inquire_cred

*   Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.14-1
-   Upgrade version

*   Tue Oct 07 2014 Divya Thaluru <dthaluru@vmware.com> 1.12.2-1
-   Initial build. First version
