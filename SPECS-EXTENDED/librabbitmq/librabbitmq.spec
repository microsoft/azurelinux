Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# Fedora spec file for librabbitmq
#
# Copyright (c) 2012-2024 Remi Collet
# License: CC-BY-SA-4.0
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%bcond_without      tests

%global gh_commit   124722b5045baa41a24ce2e2d7c52a47467e7ac0
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    alanxz
%global gh_project  rabbitmq-c
%global libname     librabbitmq
%global soname      4

Name:      %{libname}
Summary:   Client library for AMQP
Version:   0.14.0
Release:   1%{?dist}
License:   MIT
URL:       https://github.com/alanxz/rabbitmq-c

Source0:   https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz


BuildRequires: gcc
BuildRequires: cmake >= 3.22
BuildRequires: openssl-devel >= 1.1.1
# For tools
BuildRequires: popt-devel >= 1.14
# For man page
BuildRequires: xmlto
BuildRequires: make


%description
This is a C-language AMQP client library for use with AMQP servers
speaking protocol versions 0-9-1.


%package devel
Summary:    Header files and development libraries for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{name}.


%package tools
Summary:    Example tools built using the librabbitmq package
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description tools
This package contains example tools built using %{name}.

It provides:
amqp-consume        Consume messages from a queue on an AMQP server
amqp-declare-queue  Declare a queue on an AMQP server
amqp-delete-queue   Delete a queue from an AMQP server
amqp-get            Get a message from a queue on an AMQP server
amqp-publish        Publish a message on an AMQP server


%prep
%setup -q -n %{gh_project}-%{gh_commit}

# Copy sources to be included in -devel docs.
cp -pr examples Examples

# This test requires a running server
sed -e '/test_basic/d' -i tests/CMakeLists.txt


%build
# static lib required for tests
%cmake \
  -DBUILD_TOOLS:BOOL=ON \
  -DBUILD_TOOLS_DOCS:BOOL=ON \
%if %{with tests}
  -DINSTALL_STATIC_LIBS:BOOL=OFF \
%else
  -DBUILD_TESTING:BOOL=OFF \
  -DBUILD_STATIC_LIBS:BOOL=OFF \
%endif
  -S .

%if 0%{?cmake_build:1}
%cmake_build
%else
make %{_smp_mflags}
%endif


%install
%if 0%{?cmake_install:1}
%cmake_install
%else
make install  DESTDIR="%{buildroot}"
%endif


%check
: check .pc is usable
grep @ %{buildroot}%{_libdir}/pkgconfig/librabbitmq.pc && exit 1
grep %{version} %{buildroot}%{_libdir}/pkgconfig/librabbitmq.pc || exit 1
: check cmake files are usable
grep static %{buildroot}%{_libdir}/cmake/rabbitmq-c/*.cmake && exit 1
 

%if %{with tests}
: upstream tests
%if 0%{?ctest:1}
%ctest
%else
make test
%endif
%else
: Tests disabled
%endif


%files
%license LICENSE
%{_libdir}/%{libname}.so.%{soname}
%{_libdir}/%{libname}.so.%{version}


%files devel
%doc AUTHORS THANKS *.md
%doc Examples
%{_libdir}/%{libname}.so
%{_includedir}/amqp*
%{_includedir}/rabbitmq-c
%{_libdir}/pkgconfig/%{libname}.pc
%{_libdir}/cmake/rabbitmq-c

%files tools
%{_bindir}/amqp-*
%doc %{_mandir}/man1/amqp-*.1*
%doc %{_mandir}/man7/librabbitmq-tools.7*


%changelog
* Tue Nov 12 2024 Sumit Jena <v-sumitjena@microsoft.com> - 0.14.0-1
- Update to version 0.14.0

* Mon Jan 24 2022 Thomas Crain <thcrain@microsoft.com> - 0.10.0-4
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.10.0-3
- Initial CBL-Mariner import from Fedora 32 (license: CC-BY-SA).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec  2 2019 Remi Collet <remi@remirepo.net> - 0.10.0-1
- update to 0.10.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb  4 2019 Remi Collet <remi@remirepo.net> - 0.9.0-3
- fix cmake invocation and FTBFS

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May 15 2018 Remi Collet <remi@remirepo.net> - 0.9.0-1
- update to 0.9.0

* Tue Feb 20 2018 Remi Collet <remi@remirepo.net> - 0.8.0-7
- missing BR on C compiler

* Thu Feb 15 2018 Remi Collet <remi@remirepo.net> - 0.8.0-6
- drop ldconfig scriptlets

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Apr 12 2016 Remi Collet <remi@fedoraproject.org> - 0.8.0-1
- update to 0.8.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 0.7.1-1
- update to 0.7.1

* Fri Jul  3 2015 Remi Collet <remi@fedoraproject.org> - 0.7.0-1
- update to 0.7.0
- swicth to cmake
- switch from upstream tarball to github sources

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 20 2015 Remi Collet <remi@fedoraproject.org> - 0.6.0-1
- update to 0.6.0
- soname changed to .4

* Mon Sep 15 2014 Remi Collet <remi@fedoraproject.org> - 0.5.2-1
- update to 0.5.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Remi Collet <remi@fedoraproject.org> - 0.5.1-1
- update to 0.5.1
- fix license handling
- move all documentation in devel subpackage

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Remi Collet <remi@fedoraproject.org> - 0.5.0-2
- upstream patch for missing function

* Mon Feb 17 2014 Remi Collet <remi@fedoraproject.org> - 0.5.0-1
- update to 0.5.0
- open https://github.com/alanxz/rabbitmq-c/issues/169 (version is 0.5.1-pre)
- open https://github.com/alanxz/rabbitmq-c/issues/170 (amqp_get_server_properties)

* Mon Jan 13 2014 Remi Collet <remi@fedoraproject.org> - 0.4.1-4
- drop BR python-simplejson

* Tue Jan  7 2014 Remi Collet <remi@fedoraproject.org> - 0.4.1-3
- fix broken librabbitmq.pc, #1039555
- add check for usable librabbitmq.pc

* Thu Jan  2 2014 Remi Collet <remi@fedoraproject.org> - 0.4.1-2
- fix Source0 URL

* Sat Sep 28 2013 Remi Collet <remi@fedoraproject.org> - 0.4.1-1
- update to 0.4.1
- add ssl support

* Thu Aug  1 2013 Remi Collet <remi@fedoraproject.org> - 0.3.0-3
- cleanups

* Wed Mar 13 2013 Remi Collet <remi@fedoraproject.org> - 0.3.0-2
- remove tools from main package

* Wed Mar 13 2013 Remi Collet <remi@fedoraproject.org> - 0.3.0-1
- update to 0.3.0
- create sub-package for tools

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-0.2.git2059570
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 01 2012 Remi Collet <remi@fedoraproject.org> - 0.2-0.1.git2059570
- update to latest snapshot (version 0.2, moved to github)
- License is now MIT

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.3.hgfb6fca832fd2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 11 2012 Remi Collet <remi@fedoraproject.org> - 0.1-0.2.hgfb6fca832fd2
- add %%check (per review comment)

* Sat Mar 10 2012 Remi Collet <remi@fedoraproject.org> - 0.1-0.1.hgfb6fca832fd2
- Initial RPM

