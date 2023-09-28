Summary:        GNU Crypto Libraries
Name:           libgcrypt
Version:        1.9.4
Release:        2%{?dist}
License:        GPLv2+ and LGPLv2+ and BSD and MIT and Public Domain
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://gnupg.org/related_software/libgcrypt/
Source0:        https://gnupg.org/ftp/gcrypt/%{name}/%{name}-%{version}.tar.bz2
BuildRequires:  libgpg-error-devel
Requires:       libgpg-error

%description
The libgcrypt package contains a general purpose crypto library based on the code used in GnuPG. The library provides
a high level interface to cryptographic building blocks using an extendable and flexible API.

%package devel
Summary:        Development libraries and header files for libgcrypt
Requires:       %{name} = %{version}-%{release}
Requires:       libgpg-error-devel

%description devel
The package contains libraries and header files for
developing applications that use libgcrypt.

%prep
%autosetup

%build
%configure
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print
rm -rf %{buildroot}%{_infodir}

%check
%make_build check

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license COPYING COPYING.LIB LICENSES
%{_bindir}/dumpsexp
%{_bindir}/hmac256
%{_bindir}/libgcrypt-config
%{_bindir}/mpicalc
%{_libdir}/%{name}.so.20*
%{_mandir}/man1/hmac256*

%files devel
%defattr(-,root,root)
%{_includedir}/gcrypt.h
%{_datadir}/aclocal/%{name}.m4
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.9.4-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon Nov 22 2021 Thomas Crain <thcrain@microsoft.com> - 1.9.4-1
- Upgrade to latest upstream version
- License verified

* Fri Sep 10 2021 Thomas Crain <thcrain@microsoft.com> - 1.8.7-3
- Remove libtool archive files from final packaging

* Tue Jun 22 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.8.7-2
- libgcrypt CVE-2021-33560 fix

* Mon Feb 01 2021 Thomas Crain <thcrain@microsoft.com> - 1.8.7-1
- Update to 1.8.7 to fix CVE-2019-13627
- Remove cross-compile patch
- Add pkgconfig file to devel subpackage
- Update Source0 and URL tags, remove SHA-1 tag
- Lint spec to Mariner style

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.8.3-4
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.8.3-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Nov 06 2018 Sriram Nambakam <snambakam@vmware.com> - 1.8.3-2
- Cross compilation support

* Mon Sep 10 2018 Bo Gan <ganb@vmware.com> - 1.8.3-1
- Update to 1.8.3

* Tue Oct 10 2017 Vinay Kulkarni <kulkarniv@vmware.com> - 1.8.1-1
- Updated to v1.8.1 to address CVE-2017-0379

* Tue Apr 04 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 1.7.6-1
- Udpated to version 1.7.6

* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> - 1.6.5-3
- Required libgpg-error-devel.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.6.5-2
- GA - Bump release of all rpms

* Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  1.6.5-1
- Upgrade to 1.6.5

* Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> - 1.6.3-1
- Initial build. First version
