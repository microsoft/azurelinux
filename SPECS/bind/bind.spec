Summary:        Domain Name System software
Name:           bind
Version:        9.16.27
Release:        1%{?dist}
License:        ISC
URL:            https://www.isc.org/downloads/bind/
Source0:        https://ftp.isc.org/isc/bind9/%{version}/%{name}-%{version}.tar.xz
# CVE-2019-6470 is fixed by updating the dhcp package to 4.4.1 or greater
Patch0:         CVE-2019-6470.nopatch
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
Requires:       openssl
Requires:       libuv
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):/usr/sbin/userdel /usr/sbin/groupdel
BuildRequires:  openssl-devel
BuildRequires:  libcap-devel
BuildRequires:  python3
BuildRequires:  python-ply
BuildRequires:  libuv-devel
# Enforce fix for CVE-2019-6470
Conflicts:      dhcp < 4.4.1

%description
BIND is open source software that implements the Domain Name System (DNS) protocols
for the Internet. It is a reference implementation of those protocols, but it is
also production-grade software, suitable for use in high-volume and high-reliability applications.

%package utils
Summary: BIND utilities
%description utils
%{summary}.


%prep
%autosetup -p1
%build
./configure \
    --prefix=%{_prefix}
make -C lib/dns %{?_smp_mflags}
make -C lib/isc %{?_smp_mflags}
make -C lib/bind9 %{?_smp_mflags}
make -C lib/isccfg %{?_smp_mflags}
make -C lib/irs %{?_smp_mflags}
make -C bin/dig %{?_smp_mflags}
%install
make -C bin/dig DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
mkdir -p %{buildroot}/%{_sysconfdir}
mkdir -p %{buildroot}/%{_prefix}/lib/tmpfiles.d
cat << EOF >> %{buildroot}/%{_sysconfdir}/named.conf
zone "." in {
    type master;
    allow-update {none;}; // no DDNS by default
};
EOF
echo "d /run/named 0755 named named - -" > %{buildroot}/%{_prefix}/lib/tmpfiles.d/named.conf

%pre
if ! getent group named >/dev/null; then
    groupadd -r named
fi
if ! getent passwd named >/dev/null; then
    useradd -g named -d /var/lib/bind\
        -s /bin/false -M -r named
fi
%post -p /sbin/ldconfig

%postun
/sbin/ldconfig
if getent passwd named >/dev/null; then
    userdel named
fi
if getent group named >/dev/null; then
    groupdel named
fi

%files utils
%defattr(-,root,root)
%license LICENSE
%{_bindir}/*
%{_sysconfdir}/*
%{_prefix}/lib/tmpfiles.d/named.conf

%changelog
* Thu Mar 17 2022 Muhammad Falak <mwani@microsoft.com> - 9.16.27-1
- Bump version to 9.16.27 to address CVE-2021-25220 & CVE-2022-0396

* Tue Nov 09 2021 Nick Samson <nisamson@microsoft.com> - 9.16.22-1
- Upgrade to 9.16.22, fixing CVE-2021-25219. Removed file entries removed from source build. Removed unnecessary patch files.

* Wed May 12 2021 Andrew Phelps <anphel@microsoft.com> - 9.16.15-1
- Update version to 9.16.15 to fix CVE-2021-25215

* Mon Mar 01 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 9.16.3-3
- Fixes CVE-2020-8625

* Fri Sep 11 2020 Ruying Chen <v-ruyche@microsoft.com> - 9.16.3-2
- Fixes CVE-2020-8618, CVE-2020-8619, CVE-2020-8620,
- CVE-2020-8621, CVE-2020-8622, CVE-2020-8623, CVE-2020-8624

* Wed May 27 2020 Daniel McIlvaney <damcilva@microsoft.com> - 9.16.3-1
- Update to version 9.16.3, fixes CVE-2018-5743, CVE-2018-5744, CVE-2019-6465, CVE-2019-6467, CVE-2019-6471, CVE-2020-8616, CVE-2020-8617

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 9.13.3-4
- Added %%license line automatically

* Fri May  1 2020 Emre Girgin <mrgirgin@microsoft.com> 9.13.3-3
- Renaming bindutils to bind.
- Add bind-utils subpackage.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 9.13.3-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 23 2018 Sujay G <gsujay@vmware.com> 9.13.3-1
- Bump bindutils version to 9.13.3

* Mon Feb 12 2018 Xiaolin Li <xiaolinl@vmware.com> 9.10.6-1
- Upgrading version to 9.10.6-P1, fix CVE-2017-3145

* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 9.10.4-4
- Remove shadow from requires and use explicit tools for post actions

* Fri Apr 14 2017 Kumar Kaushik <kaushikk@vmware.com> 9.10.4-3
- Upgrading version to 9.10.4-P8

* Mon Nov 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 9.10.4-2
- add shadow to requires

* Mon Jun 06 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 9.10.4-1
- Upgraded the version to 9.10.4

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 9.10.3-3
- GA - Bump release of all rpms

* Fri Apr 29 2016 Xiaolin Li <xiaolinl@vmware.com> 9.10.3-2
- Add group named and user named

* Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 9.10.3-1
- Updated to version 9.10.3

* Tue Aug 11 2015 Divya Thaluru <dthaluru@vmware.com> 9.10.1-1
- Fixing release

* Tue Jan 20 2015 Divya Thaluru <dthaluru@vmware.com> 9.10.1-P1
- Initial build. First version
