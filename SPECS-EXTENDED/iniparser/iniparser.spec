Vendor:         Microsoft Corporation
Distribution:   Mariner
# Set --with test to run the Samba torture testsuite.
%bcond_with testsuite

Name:		iniparser
Version:	4.1
Release:	6%{?dist}
Summary:	C library for parsing "INI-style" files

License:	MIT
URL:		https://github.com/ndevilla/%{name}
Source0:	https://github.com/ndevilla/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:	gcc

%description
iniParser is an ANSI C library to parse "INI-style" files, often used to
hold application configuration information.

%package devel
Summary:	Header files, libraries and development documentation for %{name}
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q

%build
# remove library rpath from Makefile
sed -i 's|-Wl,-rpath -Wl,/usr/lib||g' Makefile
sed -i 's|-Wl,-rpath,/usr/lib||g' Makefile
# set the CFLAGS to Fedora standard
sed -i 's|^CFLAGS|CFLAGS = %{optflags} -fPIC\nNOCFLAGS|' Makefile
make %{?_smp_mflags}

%install
# iniParser doesn't have a 'make install' of its own :(
install -d %{buildroot}%{_includedir}/%{name} %{buildroot}%{_libdir}
install -m 644 -t %{buildroot}%{_includedir}/%{name} src/dictionary.h src/iniparser.h
ln -s %{name}/dictionary.h %{buildroot}%{_includedir}/dictionary.h
ln -s %{name}/iniparser.h %{buildroot}%{_includedir}/iniparser.h
install -m 755 -t %{buildroot}%{_libdir}/ libiniparser.so.1
ln -s libiniparser.so.1 %{buildroot}%{_libdir}/libiniparser.so

%if %{with testsuite}
%check
make
make check
./test/iniexample
./test/parse test/twisted.ini
%endif

%ldconfig_scriptlets

%files
%doc README.md INSTALL AUTHORS
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_libdir}/libiniparser.so.1

%files devel
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_libdir}/libiniparser.so
%{_includedir}/%{name}
%{_includedir}/*.h

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.1-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov  8 2018 Robin Lee <cheeselee@fedoraproject.org> - 4.1-2
- Add symlinks for headers to be compitable with Debian (BZ#1635706)

* Fri Aug 31 2018 Robin Lee <cheeselee@fedoraproject.org> - 4.1-1
- Update to 4.1 (BZ#1508863)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-6.20160821git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-5.20160821git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-4.20160821git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-3.20160821git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-2.20160821git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Aug 21 2016 Jaromír Cápík <jaromir.capik@email.cz> - 4.0-1.20160821git
- Update to 4.0 [git e24843b] (#1346451)
- Spec file maintenance

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jan 10 2014 - Andreas Schneider <asn@redhat.com> - 3.1-4
- resolves: #1031119 - Fix possible crash with crafted ini files.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 10 2012 Jaromir Capik <jcapik@redhat.com> - 3.1-1
- Update to 3.1
- Minor spec file changes according to the latest guidelines

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Simo Sorce <ssorce@redhat.com> - 3.0-1
- Final 3.0 release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.4.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.3.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.2.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jan 26 2009 Alex Hudson <fedora@alexhudson.com> - 3.0-0.1.b
- change version number to reflect "pre-release" status

* Mon Jan 19 2009 Alex Hudson <fedora@alexhudson.com> - 3.0b-3
- ensure LICENSE file is installed

* Wed Jan 14 2009 Alex Hudson <fedora@alexhudson.com> - 3.0b-2
- respond to review: added -fPIC to cflags, used 'install'

* Tue Jan 13 2009 Alex Hudson <fedora@alexhudson.com> - 3.0b-1
- Initial packaging attempt
