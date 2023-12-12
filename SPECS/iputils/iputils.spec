Summary:        Programs for basic networking
Name:           iputils
Version:        20211215
Release:        2%{?dist}
License:        BSD-3 AND GPLv2+ AND Rdisc
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Communications
URL:            https://github.com/iputils/iputils
Source0:        https://github.com/iputils/iputils/archive/20211215.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         ping_test_ipv6_localhost.patch
BuildRequires:  iproute
BuildRequires:  libcap-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libxslt
BuildRequires:  meson
BuildRequires:  ninja-build
Requires:       libcap
Requires:       libgcrypt
Obsoletes:      inetutils

%description
The Iputils package contains programs for basic networking.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%meson
%meson_build

%install
%meson_install

# rdisc and ninfod installed in sbin by default
ln -sf ../bin/tracepath %{buildroot}%{_sbindir}/tracepath
ln -sf ../bin/tracepath %{buildroot}%{_sbindir}/tracepath6
ln -sf ../bin/arping %{buildroot}%{_sbindir}/arping
ln -sf ../bin/clockdiff %{buildroot}%{_sbindir}/clockdiff
# Add ping6 into bin
ln -sf ../bin/ping %{buildroot}%{_bindir}/ping6

iconv -f ISO88591 -t UTF8 Documentation/RELNOTES.old -o RELNOTES.tmp
touch -r Documentation/RELNOTES.old RELNOTES.tmp
mv -f RELNOTES.tmp RELNOTES.old

%check
# "ping -6 -c1 localhost" fails due to hostname mapping. See patch.
%meson_test

%files
%defattr(-,root,root)
%license LICENSE
%doc RELNOTES.old
%{_sbindir}/rdisc
%{_sbindir}/ninfod
%{_sbindir}/tracepath
%{_sbindir}/tracepath6
%{_bindir}/tracepath
%caps(cap_net_raw=p) %{_bindir}/clockdiff
%{_sbindir}/clockdiff
%caps(cap_net_raw=p) %{_bindir}/arping
%{_sbindir}/arping
%caps(cap_net_raw=p cap_net_admin=p) %{_bindir}/ping
%caps(cap_net_raw=p cap_net_admin=p) %{_bindir}/ping6
%exclude %{_datadir}/locale/
%exclude %{_sysconfdir}/init.d/ninfod.sh

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 20211215-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue Feb 15 2022 Rachel Menge <rachelmenge@microsoft.com> - 20211215-1
- Update source to 20211215
- Enable meson builds and tests

* Wed Jul 29 2020 Andrew Phelps 20180629-5
- Add ping6 symlink.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 20180629-4
- Added %%license line automatically

* Mon Apr 13 2020 Jon Slobodzian <joslobo@microsoft.com> 20180629-3
- Verified license. Removed sha1. Fixed commented out URL. Fixed formatting.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 20180629-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Sep 06 2018 Ankit Jain <ankitja@vmware.com> 20180629-1
- Updated to version 20180629

* Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 20151218-4
- Remove openssl and gnutls deps

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 20151218-3
- GA - Bump release of all rpms

* Thu Apr 07 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 20151218-2
- Fixing permissions for binaries

* Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 20151218-1
- Updated to version 2.4.18

* Tue Oct 20 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 20121221-1
- Initial build.    First version
