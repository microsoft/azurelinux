Name: enca
Summary: Character set analyzer and detector
Version: 1.19
Release: 6%{?dist}
License: GPLv2
Source: https://dl.cihar.com/enca/enca-%{version}.tar.xz
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL: https://cihar.com/software/enca

BuildRequires: gcc


%description
Enca is an Extremely Naive Charset Analyser. It detects character set and
encoding of text files and can also convert them to other encodings using
either a built-in converter or external libraries and tools like libiconv,
librecode, or cstocs.

Currently, it has support for Belarussian, Bulgarian, Croatian, Czech,
Estonian, Latvian, Lithuanian, Polish, Russian, Slovak, Slovene, Ukrainian,
Chinese and some multibyte encodings (mostly variants of Unicode)
independent on the language.

This package also contains shared Enca library other programs can make use of.

Install %{name} if you need to cope with text files of dubious origin
and unknown encoding and convert them to some reasonable encoding.


%package devel
Summary: Header files and libraries for %{name} charset analyzer
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The %{name}-devel package contains the header files for writing
programs using the Extremely Naive Charset Analyser library,
and its API documentation.

Install %{name}-devel if you are going to create applications using the Enca
library.


%prep
%setup -q


%build

%configure \
	--disable-dependency-tracking \
	--disable-rpath \
	--without-librecode \
	--disable-external \
	--disable-static \
	--disable-gtk-doc

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install

make install DESTDIR=$RPM_BUILD_ROOT HTML_DIR=/tmp/html

rm -rf $RPM_BUILD_ROOT/tmp/html
rm -rf $RPM_BUILD_ROOT/%{_libexecdir}
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la


%check
make check LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_libdir}


%ldconfig_scriptlets


%files
%{_bindir}/*
%{_libdir}/libenca.so.*
%{_mandir}/*/*
%doc AUTHORS COPYING FAQ README THANKS TODO

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%doc DEVELOP.md


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.19-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 28 2018 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.19-1
- update to 1.19
- avoid rpath in binaries

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.18-5
- Switch to %%ldconfig_scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 10 2016 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.18-1
- update to 1.18

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Sep 10 2015 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.16-1
- update to 1.16

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 19 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.15-1
- update to 1.15

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar  5 2013 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.14-1
- update to 1.14

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Mar 29 2010 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.13-1
- update to 1.13

* Tue Aug 25 2009 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.10-1
- Update to 1.10
- Change urls for new upstream

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.9-4
- Autorebuild for GCC 4.3

* Thu Aug 16 2007 Dmitry Butskoy <Dmitry@Butskoy.name>
- Change License tag to GPLv2

* Fri Sep  1 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.9-3
- rebuild for FC6

* Tue Feb 14 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.9-2
- rebuild for FC5

* Mon Dec 19 2005 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.9-1
- upgrade to 1.9

* Mon Nov 28 2005 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.8-1
- upgrade to 1.8
- update description
