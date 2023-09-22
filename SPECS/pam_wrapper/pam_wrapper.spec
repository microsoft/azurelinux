Name:           pam_wrapper
Version:        1.1.4
Release:        2%{?dist}
Summary:        A tool to test PAM applications and PAM modules
License:        GPLv3+
URL:            https://cwrap.org/
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://ftp.samba.org/pub/cwrap/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  gnupg2
BuildRequires:  libcmocka-devel
BuildRequires:  pam-devel
BuildRequires:  python3-devel

Recommends:     cmake
Recommends:     pkgconfig

%description
This component of cwrap allows you to either test your PAM (Linux-PAM
and OpenPAM) application or module.

For testing PAM applications, simple PAM module called pam_matrix is
included. If you plan to test a PAM module you can use the pamtest library,
which simplifies testing of modules. You can combine it with the cmocka
unit testing framework or you can use the provided Python bindings to
write tests for your module in Python.

%package -n libpamtest
Summary:        A tool to test PAM applications and PAM modules
License:        GPLv3+
Requires:       pam_wrapper = %{version}-%{release}

%description -n libpamtest
If you plan to test a PAM module you can use this library, which simplifies
testing of modules.

%package -n libpamtest-devel
Summary:        A tool to test PAM applications and PAM modules
License:        GPLv3+
Requires:       libpamtest = %{version}-%{release}
Requires:       pam_wrapper = %{version}-%{release}

Recommends:     cmake
Recommends:     pkgconfig

%description -n libpamtest-devel
If you plan to develop tests for a PAM module you can use this library,
which simplifies testing of modules. This sub package includes the header
files for libpamtest.

%package -n libpamtest-doc
Summary:        The libpamtest API documentation
License:        GPLv3+

%description -n libpamtest-doc
Documentation for libpamtest development.

%package -n python3-libpamtest
Summary:        A python wrapper for libpamtest
License:        GPLv3+
Requires:       libpamtest = %{version}-%{release}
Requires:       pam_wrapper = %{version}-%{release}

%description -n python3-libpamtest
If you plan to develop python tests for a PAM module you can use this
library, which simplifies testing of modules. This subpackage includes
the header files for libpamtest

%prep
%autosetup -S git

%build
if test ! -e "obj"; then
  mkdir obj
fi
pushd obj
%cmake \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DUNIT_TESTING=ON \
  %{_builddir}/%{name}-%{version}

make %{?_smp_mflags} VERBOSE=1
make doc VERBOSE=1
popd

%install
pushd obj
make DESTDIR=%{buildroot} install
popd

%ldconfig_scriptlets

%ldconfig_scriptlets -n libpamtest

%check
pushd obj
ctest --output-on-failure
popd

%files
%license LICENSE
%{_libdir}/libpam_wrapper.so*
%{_libdir}/pkgconfig/pam_wrapper.pc
%dir %{_libdir}/cmake/pam_wrapper
%{_libdir}/cmake/pam_wrapper/pam_wrapper-config-version.cmake
%{_libdir}/cmake/pam_wrapper/pam_wrapper-config.cmake
%{_libdir}/pam_wrapper/pam_chatty.so
%{_libdir}/pam_wrapper/pam_matrix.so
%{_libdir}/pam_wrapper/pam_get_items.so
%{_libdir}/pam_wrapper/pam_set_items.so
%{_mandir}/man1/pam_wrapper.1*
%{_mandir}/man8/pam_chatty.8*
%{_mandir}/man8/pam_matrix.8*
%{_mandir}/man8/pam_get_items.8*
%{_mandir}/man8/pam_set_items.8*

%files -n libpamtest
%{_libdir}/libpamtest.so.*

%files -n libpamtest-devel
%{_libdir}/libpamtest.so
%{_libdir}/pkgconfig/libpamtest.pc
%dir %{_libdir}/cmake/pamtest
%{_libdir}/cmake/pamtest/pamtest-config-relwithdebinfo.cmake
%{_libdir}/cmake/pamtest/pamtest-config-version.cmake
%{_libdir}/cmake/pamtest/pamtest-config.cmake
%{_includedir}/libpamtest.h

%files -n libpamtest-doc
%license LICENSE
%doc obj/doc/html

%files -n python3-libpamtest
%{python3_sitearch}/pypamtest.so

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.1.4-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon Jul 25 2022 Sumedh Sharma <sumsharma@microsoft.com> - 1.1.4-1
- Bumping version to 1.1.4.
- Remove gpg signature verification
- License verified
 
* Tue Jun 08 2021 Thomas Crain <thcrain@microsoft.com> - 1.1.3-3
- Remove python2 macros

* Mon Jan 04 2021 Joe Schmitt <joschmit@microsoft.com> - 1.1.3-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove python2 support

* Thu Mar 26 2020 Andreas Schneider <asn@redhat.com> - 1.1.3-1
- Update to version 1.1.3
  * https://gitlab.com/cwrap/pam_wrapper/-/blob/master/CHANGELOG
  * resolves: #1816943

* Tue Mar 24 2020 Andreas Schneider <asn@redhat.com> - 1.1.2-1
- Update to version 1.1.2
  * https://gitlab.com/cwrap/pam_wrapper/-/blob/master/CHANGELOG

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 22 2020 Bastien Nocera <bnocera@redhat.com> - 1.0.7-5
+ pam_wrapper-1.0.7-5
- Fix crash in pam_wrapper

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.7-4
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 26 2018 Andreas Schneider <asn@redhat.com> - 1.0.7-1
- Update to version 1.0.7
- resolves: #1627401 - Create python3 packages

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Apr  7 2017 Jakub Hrozek <jakub.hrozek@posteo.se> - 1.0.3-1
- New upstream release 1.0.3

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jun  2 2016 Jakub Hrozek <jakub.hrozek@posteo.se> - 1.0.2-1
- New upstream release 1.0.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Jakub Hrozek <jakub.hrozek@posteo.se> - 1.0.1-2
- Fix review comments from rhbz#1299637

* Mon Jan 18 2016 Jakub Hrozek <jakub.hrozek@posteo.se> - 1.0.1-1
- New upstream release

* Wed Dec 16 2015 Jakub Hrozek <jakub.hrozek@posteo.se> - 1.0.0-1
- Initial packaging
