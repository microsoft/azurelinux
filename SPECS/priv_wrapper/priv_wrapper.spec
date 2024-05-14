Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           priv_wrapper
Version:        1.0.1
Release:        5%{?dist}

Summary:        A library to disable resource limits and other privilege dropping
License:        GPLv3+
Url:            https://cwrap.org/

Source0:        https://ftp.samba.org/pub/cwrap/%{name}-%{version}.tar.gz
Source1:        https://ftp.samba.org/pub/cwrap/%{name}-%{version}.tar.gz.asc
Source2:        priv_wrapper.keyring

Patch0:         priv_wrapper-fix-cmocka-1.1.6+-support.patch

BuildRequires:  gcc
BuildRequires:  cmake
BuildRequires:  gnupg2
BuildRequires:  libcmocka-devel >= 1.1.0

Recommends:     cmake
Recommends:     pkgconfig

%description
priv_wrapper aims to help running processes which are dropping privileges or
are restricting resources in test environments.
It can disable chroot, prctl, pledge and setrlmit system calls. A disabled call
always succeeds (i.e. returns 0) and does nothing.
The system call pledge exists only on OpenBSD.

To use it, set the following environment variables:

LD_PRELOAD=libpriv_wrapper.so
PRIV_WRAPPER_CHROOT_DISABLE=1

This package does not have a devel package, because this project is for
development/testing.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1

%build
if test ! -e "obj"; then
  mkdir obj
fi

pushd obj

%cmake .. \
  -DUNIT_TESTING=ON

%cmake_build

popd

%install
pushd obj
%cmake_install
popd

%ldconfig_scriptlets

%check
pushd obj
%ctest
popd

%files
%doc AUTHORS README.md CHANGELOG.md
%license LICENSE
%{_libdir}/libpriv_wrapper.so*
%dir %{_libdir}/cmake
%dir %{_libdir}/cmake/priv_wrapper
%{_libdir}/cmake/priv_wrapper/priv_wrapper-config-version.cmake
%{_libdir}/cmake/priv_wrapper/priv_wrapper-config.cmake
%dir %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/priv_wrapper.pc
%{_mandir}/man1/priv_wrapper.1*

%changelog
* Fri May 26 2023 Vince Perri <viperri@microsoft.com> - 0.10.5-2
- License verified.
- Switched to out-of-source build.
- Initial CBL-Mariner import from Fedora 39 (license: MIT).

* Mon Mar 06 2023 Andreas Schneider <asn@redhat.com> - 1.0.1-4
- Update License to SPDX expression

* Mon Feb 27 2023 Andreas Schneider <asn@redhat.com> - 1.0.1-3
- Fix building with cmocka >= 1.1.6

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Nov 24 2022 Pavel Filipenský <pfilipenn@redhat.com> - 1.0.1-1
- Update to version 1.0.1

* Thu Nov 10 2022 Pavel Filipenský <pfilipen@redhat.com> - 1.0.0-3
- Patch prctl() on ppc64le

* Tue Oct 25 2022 Pavel Filipenský <pfilipen@redhat.com> - 1.0.0-2
- Verify packages using gpgverify
- Make description line length < 80

* Mon Oct 24 2022 Pavel Filipenský <pfilipen@redhat.com> -  1.0.0-1
- Initial package
