Summary:        High-Level Crypto API
Name:           gpgme
Version:        1.16.0
Release:        2%{?dist}
License:        GPLv3+ and LGPLv2+ and MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://www.gnupg.org/(it)/related_software/gpgme/index.html
Source0:        https://www.gnupg.org/ftp/gcrypt/%{name}/%{name}-%{version}.tar.bz2
BuildRequires:  gnupg2
BuildRequires:  libassuan-devel >= 2.4.2
BuildRequires:  libgpg-error-devel >= 1.36
BuildRequires:  python3-devel
BuildRequires:  swig
Requires:       libassuan >= 2.4.2
Requires:       libgpg-error >= 1.36
Requires:       gnupg2

%description
The GPGME package is a C language library that allows to add support for cryptography to a program. It is designed to make access to public key crypto engines like GnuPG or GpgSM easier for applications. GPGME provides a high-level crypto API for encryption, decryption, signing, signature verification and key management.

%package    devel
Group:      Development/Libraries
Summary:    Static libraries and header files from GPGME, GnuPG Made Easy.
Requires:   %{name} = %{version}-%{release}
Requires:   libgpg-error-devel >= 1.32

%description 	devel
Static libraries and header files from GPGME, GnuPG Made Easy.

%package -n     python3-gpg
Summary:        GPG bindings for Python 3
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description -n python3-gpg
%{summary}.

%prep
%autosetup
sed -i 's/defined(__FreeBSD__)/defined(__FreeBSD__) || defined(__GLIBC__)/g' src/posix-io.c

%build
%configure \
    --enable-languages=cl,python \
    --disable-fd-passing \
    --disable-static \
    --disable-silent-rules \
    --disable-gpgsm-test
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print
rm -rf %{buildroot}/%{_infodir}

%ldconfig_scriptlets

%check
cd tests
%make_build check-TESTS

%files
%defattr(-,root,root)
%license AUTHORS COPYING COPYING.LESSER LICENSES
%{_libdir}/*.so.11*

%files devel
%defattr(-,root,root)
%{_bindir}/%{name}-config
%{_bindir}/%{name}-json
%{_bindir}/%{name}-tool
%{_datadir}/aclocal/%{name}.m4
%{_datadir}/common-lisp/source/gpgme/*
%{_includedir}/%{name}.h
%{_libdir}/libgpgme.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-glib.pc

%files -n python3-gpg
%doc lang/python/README
%{python3_sitearch}/gpg-*.egg-info
%{python3_sitearch}/gpg/

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.16.0-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon Nov 22 2021 Thomas Crain <thcrain@microsoft.com> - 1.16.0-1
- Upgrade to latest upstream version
- Lint spec
- License verified

* Fri Oct 22 2021 Andrew Phelps <anphel@microsoft.com> - 1.13.1-8
- Fix issue with glibc 2.34

* Wed May 19 2021 Nick Samson <nisamson@microsoft.com> - 1.13.1-7
- Removed python2 support

* Tue Nov 10 2020 Andrew Phelps <anphel@microsoft.com> - 1.13.1-6
- Fix check test.

* Thu Aug 20 2020 Mateusz Malisz <mamalisz@microsoft.com> - 1.13.1-5
- Resolve file conflicts for shared objects.

* Wed May 13 2020 Emre Girgin <mrgirgin@microsoft.com> - 1.13.1-4
- Add python-gpg subpackage.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.13.1-3
- Added %%license line automatically

* Tue Apr 21 2020 Nicolas Ontiveros <niontive@microsoft.com> - 1.13.1-2
- Use gnupg2 for Requires and BR.

* Fri Apr 17 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.13.1-1
- Upgrading to version 1.13.1.
- Removed 'sha1' macro.
- Added building the 'python3-gpg' subpackage.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.11.1-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sat Oct 20 2018 Ankit Jain <ankitja@vmware.com> - 1.11.1-2
- Removed gpg2, gnupg-2.2.10 doesn't provide gpg2

* Tue Sep 11 2018 Anish Swaminathan <anishs@vmware.com> - 1.11.1-1
- Update version to 1.11.1

* Wed Aug 30 2017 Alexey Makhalov <amakhalov@vmware.com> - 1.9.0-3
- Add requires gnupg

* Thu Apr 20 2017 Alexey Makhalov <amakhalov@vmware.com> - 1.9.0-2
- Disabe C++ bindings

* Thu Apr 13 2017 Danut Moraru <dmoraru@vmware.com> - 1.9.0-1
- Update to version 1.9.0

* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> - 1.6.0-3
- Required libgpg-error-devel.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.6.0-2
- GA - Bump release of all rpms

* Thu Jan 14 2016 Xiaolin Li <xiaolinl@vmware.com> - 1.6.0-1
- Updated to version 1.6.0

* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> - 1.5.3-2
- Updated group.

* Tue Dec 30 2014 Divya Thaluru <dthaluru@vmware.com> - 1.5.3-1
- Initial version
