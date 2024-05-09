Vendor:         Microsoft Corporation
Distribution:   Azure Linux

Name:		openwsman
Version:	2.6.8
Release:	13%{?dist}
Summary:	Open source Implementation of WS-Management

License:	BSD
URL:		https://www.openwsman.org/
Source0:	https://github.com/Openwsman/openwsman/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# help2man generated manpage for openwsmand binary
Source1:	openwsmand.8.gz
# service file for systemd
Source2:	openwsmand.service
# script for testing presence of the certificates in ExecStartPre
Source3:	owsmantestcert.sh
Patch1:		openwsman-2.4.0-pamsetup.patch
Patch2:		openwsman-2.4.12-ruby-binding-build.patch
Patch3:		openwsman-2.6.2-openssl-1.1-fix.patch
Patch4:		openwsman-2.6.5-http-status-line.patch
Patch5:		openwsman-2.6.5-libcurl-error-codes-update.patch
Patch6:		openwsman-2.6.8-CVE-2019-3816.patch
Patch7:		openwsman-2.6.8-CVE-2019-3833.patch
BuildRequires:	swig
BuildRequires:	libcurl-devel libxml2-devel pam-devel sblim-sfcc-devel
BuildRequires:	python3 python3-devel perl-interpreter
BuildRequires:	perl-devel perl-generators pkgconfig openssl-devel
BuildRequires:	cmake
BuildRequires:	systemd-units
BuildRequires:	gcc gcc-c++

%description
Openwsman is a project intended to provide an open-source
implementation of the Web Services Management specification
(WS-Management) and to expose system management information on the
Linux operating system using the WS-Management protocol. WS-Management
is based on a suite of web services specifications and usage
requirements that exposes a set of operations focused on and covers
all system management aspects.

%package -n libwsman1
License:	BSD
Summary:	Open source Implementation of WS-Management
Provides:	%{name} = %{version}-%{release}
Obsoletes:	%{name} < %{version}-%{release}

%description -n libwsman1
Openwsman library for packages dependent on openwsman.

%package -n libwsman-devel
License:	BSD
Summary:	Open source Implementation of WS-Management
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel < %{version}-%{release}
Requires:	libwsman1 = %{version}-%{release}
Requires:	%{name}-server = %{version}-%{release}
Requires:	%{name}-client = %{version}-%{release}
Requires:	sblim-sfcc-devel libxml2-devel pam-devel
Requires:	libcurl-devel

%description -n libwsman-devel
Development files for openwsman.

%package client
License:	BSD
Summary:	Openwsman Client libraries

%description client
Openwsman Client libraries.

%package server
License:	BSD
Summary:	Openwsman Server and service libraries
Requires:	libwsman1 = %{version}-%{release}

%description server
Openwsman Server and service libraries.

%package python3
License:	BSD
Summary:	Python bindings for openwsman client API
Requires:	%{__python3}
Requires:	libwsman1 = %{version}-%{release}
%{?python_provide:%python_provide python3-openwsman}

%description python3
This package provides Python3 bindings to access the openwsman client API.


%package perl
License:	BSD
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Summary:	Perl bindings for openwsman client API
Requires:	libwsman1 = %{version}-%{release}

%description perl
This package provides Perl bindings to access the openwsman client API.


%prep
%setup -q

%patch 1 -p1 -b .pamsetup
%patch 2 -p1 -b .ruby-binding-build
%patch 3 -p1 -b .openssl-1.1-fix
%patch 4 -p1 -b .http-status-line
%patch 5 -p1 -b .libcurl-error-codes-update
%patch 6 -p1 -b .CVE-2019-3816
%patch 7 -p1 -b .CVE-2019-3833

%build
# Removing executable permissions on .c and .h files to fix rpmlint warnings. 
chmod -x src/cpp/WsmanClient.h

rm -rf build
mkdir build

export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -DFEDORA -DNO_SSL_CALLBACK"
export CFLAGS="-D_GNU_SOURCE -fPIE -DPIE"
export LDFLAGS="$LDFLAGS -Wl,-z,now -pie"
cd build
cmake \
	-DCMAKE_INSTALL_PREFIX=/usr \
	-DCMAKE_VERBOSE_MAKEFILE=TRUE \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_C_FLAGS_RELEASE:STRING="$RPM_OPT_FLAGS -fno-strict-aliasing" \
	-DCMAKE_CXX_FLAGS_RELEASE:STRING="$RPM_OPT_FLAGS" \
	-DCMAKE_SKIP_RPATH=1 \
	-DPACKAGE_ARCHITECTURE=`uname -m` \
	-DLIB=%{_lib} \
	-DBUILD_JAVA=no \
	-DBUILD_PYTHON=no \
	..

make

# Make the freshly build openwsman libraries available to build the gem's
# binary extension.
export LIBRARY_PATH=%{_builddir}/%{name}-%{version}/build/src/lib
export CPATH=%{_builddir}/%{name}-%{version}/include/
export LD_LIBRARY_PATH=%{_builddir}/%{name}-%{version}/build/src/lib/


%install
cd build


make DESTDIR=%{buildroot} install
cd ..
rm -f %{buildroot}/%{_libdir}/*.la
rm -f %{buildroot}/%{_libdir}/openwsman/plugins/*.la
rm -f %{buildroot}/%{_libdir}/openwsman/authenticators/*.la
mkdir -p %{buildroot}%{_sysconfdir}/init.d
install -m 644 etc/openwsman.conf %{buildroot}/%{_sysconfdir}/openwsman
install -m 644 etc/openwsman_client.conf %{buildroot}/%{_sysconfdir}/openwsman
mkdir -p %{buildroot}/%{_unitdir}
install -p -m 644 %{SOURCE2} %{buildroot}/%{_unitdir}/openwsmand.service
install -m 644 etc/ssleay.cnf %{buildroot}/%{_sysconfdir}/openwsman
install -p -m 755 %{SOURCE3} %{buildroot}/%{_sysconfdir}/openwsman
# install manpage
mkdir -p %{buildroot}/%{_mandir}/man8/
cp %SOURCE1 %{buildroot}/%{_mandir}/man8/
# install missing headers
install -m 644 include/wsman-xml.h %{buildroot}/%{_includedir}/openwsman
install -m 644 include/wsman-xml-binding.h %{buildroot}/%{_includedir}/openwsman
install -m 644 include/wsman-dispatcher.h %{buildroot}/%{_includedir}/openwsman

%ldconfig_scriptlets -n libwsman1

%post server
%{?ldconfig}
%systemd_post openwsmand.service

%preun server
%systemd_preun openwsmand.service

%postun server
rm -f /var/log/wsmand.log
%systemd_postun_with_restart openwsmand.service
%{?ldconfig}

%ldconfig_scriptlets client

%files -n libwsman1
%doc AUTHORS COPYING ChangeLog README.md TODO
%{_libdir}/libwsman.so.*
%{_libdir}/libwsman_client.so.*
%{_libdir}/libwsman_curl_client_transport.so.*

%files -n libwsman-devel
%doc AUTHORS COPYING ChangeLog README.md
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.so

%files python3
%doc AUTHORS COPYING ChangeLog README.md
%{python3_sitearch}/*.so
%{python3_sitearch}/*.py
%{python3_sitearch}/__pycache__/*


%files perl
%doc AUTHORS COPYING ChangeLog README.md
%{perl_vendorarch}/openwsman.so
%{perl_vendorlib}/openwsman.pm

%files server
%doc AUTHORS COPYING ChangeLog README.md
# Don't remove *.so files from the server package.
# the server fails to start without these files.
%dir %{_sysconfdir}/openwsman
%config(noreplace) %{_sysconfdir}/openwsman/openwsman.conf
%config(noreplace) %{_sysconfdir}/openwsman/ssleay.cnf
%attr(0755,root,root) %{_sysconfdir}/openwsman/owsmangencert.sh
%attr(0755,root,root) %{_sysconfdir}/openwsman/owsmantestcert.sh
%config(noreplace) %{_sysconfdir}/pam.d/openwsman
%{_unitdir}/openwsmand.service
%dir %{_libdir}/openwsman
%dir %{_libdir}/openwsman/authenticators
%{_libdir}/openwsman/authenticators/*.so
%{_libdir}/openwsman/authenticators/*.so.*
%dir %{_libdir}/openwsman/plugins
%{_libdir}/openwsman/plugins/*.so
%{_libdir}/openwsman/plugins/*.so.*
%{_sbindir}/openwsmand
%{_libdir}/libwsman_server.so.*
%{_mandir}/man8/*

%files client
%doc AUTHORS COPYING ChangeLog README.md
%{_libdir}/libwsman_clientpp.so.*
%config(noreplace) %{_sysconfdir}/openwsman/openwsman_client.conf
%{_bindir}/winrs


%changelog
* Thu Jun 10 2021 Muhammad Falak Wani <mwani@microsoft.com> - 2.6.8-13
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove support for building ruby-gem

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 18 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.6.8-11
- F-32: rebuild against ruby27

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.6.8-10
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.6.8-9
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.6.8-7
- Perl 5.30 rebuild

* Mon Apr 01 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.6.8-6
- Add requires libwsman1 for rubygem-openwsman

* Wed Mar 13 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.6.8-5
- Fix CVE-2019-3816
  Resolves: #1687760
- Fix CVE-2019-3833
  Resolves: #1687762
- Remove Dist Tag from the oldest changelog entry

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.6.8-3
- F-30: rebuild against ruby26

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 2.6.8-2
- Rebuilt for libcrypt.so.2 (#1666033)

* Thu Nov 22 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.6.8-1
- Update to openwsman-2.6.8

* Wed Nov 14 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.6.5-10
- Reflect changes in libcurl error codes
  Resolves: #1649393

* Mon Oct 01 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.6.5-9
- Require the Python interpreter directly instead of using the package name

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 03 2018 Petr Pisar <ppisar@redhat.com> - 2.6.5-7
- Perl 5.28 rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.6.5-6
- Perl 5.28 rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.6.5-5
- Rebuilt for Python 3.7

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.6.5-4
- Rebuilt for Python 3.7

* Thu Feb 22 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.6.5-3
- Fix wrong SSL_CTX_set_cipher_list() retval check
- Add BuildRequires gcc and gcc-c++
- Explicitly disable build of java bindings (build fails if java-devel is installed)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.6.5-1
- Update to openwsman-2.6.5
- Simplify python binding build and drop python2 subpackage
- Fix malformed HTTP 200 status line

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 2.6.3-11.git4391e5c
- Rebuilt for switch to libxcrypt

* Sat Jan  6 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.6.3-10.git4391e5c
- F-28: rebuild for ruby 2.5
- Backport git patches to support ruby 2.5

* Wed Oct 04 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.6.3-9.git
- Remove unnecessary net-tools requirement
  Resolves: #1496142

* Tue Sep 12 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.6.3-8.git4391e5c
- Spec file clean up (removed RPM Groups tags, removed obsolete chkconfig/initscripts
  dependencies, improved readability, fixed indentation)
- Updated openssl-1.1 patch to support builds with older openssl versions

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.6.3-7.git4391e5c
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.6.3-6.git4391e5c
- Python 2 binary package renamed to python2-openwsman
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.3-5.git4391e5c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.3-4.git4391e5c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.6.3-3.git4391e5c
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.3-2.git4391e5c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 17 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.6.3-1.git4391e5c
- Update to openwsman-2.6.3 from upstream VCS
  (because it contains shttpd 1.42)

* Thu Jan 12 2017 Vít Ondruch <vondruch@redhat.com> - 2.6.2-11
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.4

* Mon Jan 09 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.6.2-10
- Disable SSL protocols listed in config file

* Tue Jan 03 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.6.2-9
- Port to openssl 1.1.0
  Resolves: #1383992

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.6.2-8
- Rebuild for Python 3.6

* Thu Aug 11 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.6.2-7
- Add openwsman-python3 subpackage
  Resolves: #1354481

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.2-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.6.2-5
- Perl 5.24 rebuild

* Tue Mar 22 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.6.2-4
- Remove SSL_LIB acquired by readlink from CFLAGS

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Vít Ondruch <vondruch@redhat.com> - 2.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3

* Thu Nov 05 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.6.2-1
- Update to openwsman-2.6.2

* Mon Aug 31 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.6.1-1
- Update to openwsman-2.6.1
- Review PAM rules
  (pam_pwcheck is replaced by pam_pwquality, pam_unix has no 'none' option)

* Tue Jun 16 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.6.0-1
- Update to openwsman-2.6.0

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.4.15-2
- Perl 5.22 rebuild

* Thu May 21 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.4.15-1
- Update to openwsman-2.4.15

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.4.14-2
- Rebuilt for GCC 5 C++11 ABI change

* Thu Feb 26 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.4.14-1
- Update to openwsman-2.4.14

* Mon Feb 09 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.4.12-1
- Update to openwsman-2.4.12

* Sat Jan 17 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.4.6-5
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.4.6-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.4.6-1
- Update to openwsman-2.4.6

* Fri Apr 25 2014 Vít Ondruch <vondruch@redhat.com> - 2.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Tue Mar 11 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.4.4-1
- Update to openwsman-2.4.4
- Provide rubygem-openwsman instead of openwsman-ruby (patch by Vit Ondruch)

* Wed Feb 05 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.4.3-2
- Update openwsmand man page

* Thu Jan 23 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.4.3-1
- Update to openwsman-2.4.3

* Tue Jan 07 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.4.0-3
- Start the service using SSL by default

* Mon Sep 30 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.4.0-2
- Build with full relro
- Fix provides/requires
- Fix pam.d config (patch by Ales Ledvinka)
  Resolves: #1013018

* Tue Sep 17 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.4.0-1
- Update to openwsman-2.4.0
- Fix bogus date in %%changelog

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.3.6-7
- Perl 5.18 rebuild

* Tue Mar 19 2013 Vít Ondruch <vondruch@redhat.com> - 2.3.6-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Mon Mar 18 2013 Praveen K Paladugu <praveen_paladugu@dell.com> - 2.3.6-4
- Updated the dependency for ruby bindings and introduced the java bindings.

* Wed Mar 13 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.3.6-3
- rebuild for ruby 2

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 08 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.3.6-1
- Update to openwsman-2.3.6

* Mon Sep 17 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.3.5-1
- Update to openwsman-2.3.5
- Enable ruby subpackage again

* Tue Aug 28 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.3.0-7
- Fix issues found by fedora-review utility in the spec file

* Thu Aug 23 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.3.0-6
- Use new systemd-rpm macros
  Resolves: #850405

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 2.3.0-4
- Perl 5.16 rebuild

* Mon May 28 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.3.0-3
- Rename service file

* Wed May 23 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.3.0-2
- Add systemd support

* Tue Mar 27 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.3.0-1
- Update to openwsman-2.3.0

* Thu Feb 09 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.7-4
- Fix libssl loading

* Thu Feb 09 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.7-3
- Temporarily disable ruby subpackage

* Thu Jan 26 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.7-2
- Remove unnecessary net-tools requirement
  Resolves: #784787

* Wed Jan 11 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.7-1
- Update to openwsman-2.2.7

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.2.5-3
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.2.5-2
- Perl 5.14 mass rebuild

* Wed Mar 23 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.5-1
- Update to openwsman-2.2.5

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  9 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.4-2
- Recompile with -DNO_SSL_CALLBACK

* Tue Nov 16 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.4-1
- Update to openwsman-2.2.4
- Add help2man generated manpage for openwsmand binary
- Add missing openwsman headers to libwsman-devel
- Add configuration file to openwsman-client

* Wed Sep 29 2010 jkeating - 2.2.3-9
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.3-8
- Move initscript to the right place
- Fix return values from initscript according to guidelines

* Tue Aug 10 2010 Praveen K Paladugu <praveen_paladugu@dell.com> - 2.2.3-7
- Moved the certificate generation from init script. The user will have to 
-   generate the certificate manually.

* Mon Aug  2 2010 Praveen K Paladugu <praveen_paladugu@dell.com> - 2.2.3-6
- Fixed the version checking of swig and forced all the ruby files to be 
-   installed into site{lib,arch} dirs 

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.2.3-4
- Mass rebuild with perl-5.12.0

* Thu Apr 22 2010 Praveen K Paladugu <praveen_paladugu@dell.com> - 2.2.3-3
- authors.patch: Moved all the AUTHORS info to AUTHORS file.
- Corrected the Source tag.
- Corrected the package dependencies to break cyclic dependencies.
- Fixed the default attributes.
- Fixed the preun & postun scripts, to make sure the openwsmand service
-    is stopped before the package is removed.
- Added 'condrestart' function to the init script.
- Had to let the *.so files be part of the openwsman-server becuase
-    some of the source files explicitly call out for *.so files.


* Thu Apr 15 2010 Praveen K Paladugu <praveen_paladugu@dell.com> - 2.2.3-2
- Updated the spec file to adhere to the upstream standard of breaking
- the package in server, client, lib modules 
- randfile.patch: when openwsmand daemon creates a certificate the
- first time it needs a file which have random content it. This
- is pointed to $HOME/.rnd in /etc/openwsman/ssleay.cnf. Changed this
- random file to /dev/urandom. 
- initscript.patch: patch to edit the init script so that the services
- are not started by default.


* Wed Mar  3 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.3-1
- Update to openwsman-2.2.3


* Wed Sep 23 2009 Praveen K Paladugu <praveen_paladugu@dell.com> - 2.2.0-1
- Added the new 2.2.0 sources.
- Changed the release and version numbers.

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.1.0-4
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 22 2008 Matt Domsch <Matt_Domsch@dell.com> - 2.1.0-1
- update to 2.1.0, resolves security issues

* Tue Aug 19 2008  <srinivas_ramanatha@dell.com> - 2.0.0-1
- Modified the spec file to adhere to fedora packaging guidelines.
