# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define set_javaver() \
%if 	0%{?fedora}%{?rhel} == %1 \
BuildRequires:	java-%2-openjdk-devel \
%if	%1 >= 42 \
BuildRequires:	javapackages-local-openjdk%2 \
%endif \
%endif \
%{nil}

Name:		qdbm
Version:	1.8.78
Release:	71%{?dist}
# SPDX confirmed
License:	LGPL-2.1-or-later

URL:		http://fallabs.com/qdbm/
Source0:	http://fallabs.com/qdbm/%{name}-%{version}.tar.gz
# Copied from Debian package
Patch0:		qdbm-ruby-1.9-compat.patch
# Java 13 introduced yield keyword and the original yield()
# must be called with explicit receiver
Patch1:		qdbm-1.8.78-java17-yield-usage.patch
# ruby module: conformant for c99, -Werror=implicit-int
Patch2:		qdbm-1.8.78-ruby-module-c99-conformant.patch

BuildRequires:	make
BuildRequires:	gcc-c++
BuildRequires:	zlib-devel
BuildRequires:	bzip2-devel
BuildRequires:	lzo-devel
%ifarch %java_arches
%set_javaver	43	21
%set_javaver	42	21
%set_javaver	41	21
%set_javaver	40	21
%set_javaver	39	17
%endif
# ruby-devel requires ruby-libs but not require ruby
BuildRequires:	ruby
BuildRequires:	ruby-devel
BuildRequires:	perl-devel
BuildRequires:	perl-generators
BuildRequires:	perl(ExtUtils::MakeMaker)
%ifarch %java_arches
# java related macros
BuildRequires:	javapackages-tools
%endif

Summary:	Quick Database Manager

%description
QDBM is an embedded database library compatible with GDBM and NDBM.
It features hash database and B+ tree database and is developed referring
to GDBM for the purpose of the following three points: higher processing
speed, smaller size of a database file, and simpler API.


%package devel
Summary:	Libraries and Header files for QDBM Database library
Requires:	%{name} = %{version}-%{release}

%description devel
This is the development package that provides header files and libraries
for QDBM library.


%package cgi
Summary:	CGI interface for QDBM Database
Requires:	%{name} = %{version}-%{release}
Requires:	webserver

%description cgi
This package contains a CGI interface for QDBM Database.


%package java
Summary:	QDBM Database Library for Java
Requires:	%{name} = %{version}-%{release}
Requires:	java-headless

%description java
This package contains a Java interface for QDBM Database library.

%package javadoc
Summary:	API docs for QDBM Database Library Java interface
BuildArch:	noarch

%description javadoc
This package contains the API documentation for the QDBM Database library Java
interface.


%package perl
Summary:	QDBM Database Library for Perl
Requires:	%{name} = %{version}-%{release}

%description perl
This package contains a Perl interface for QDBM Database library.


%package -n qdbm++
Summary:	QDBM Database Library for C++
Requires:	%{name} = %{version}-%{release}

%description -n qdbm++
This package contains a C++ interface for QDBM Database library.

%package -n qdbm++-devel
Summary:	Libraries and Header files for QDBM C++ interface
Requires:	qdbm++ = %{version}-%{release}

%description -n qdbm++-devel
This is the development package that provides header files and libraries
for QDBM C++ interface.


%package -n ruby-qdbm
Summary:	QDBM Database Library for Ruby
Requires:	%{name} = %{version}-%{release}
Requires:	ruby(release)
Provides:	ruby(qdbm) = %{version}-%{release}

%description -n ruby-qdbm
This package contains a Ruby interface for QDBM Database library.


%prep
%autosetup -p1

# Fix path in doc/index*.html
sed -i.link  \
	-e 's|"spex|"../%{name}-devel-%{version}/spex|' \
	-e 's|"xspex|"../%{name}++-devel-%{version}/xspex|' \
	-e 's|"jspex|"../%{name}-java-%{version}/jspex|' \
	-e 's|"plspex|"../%{name}-perl-%{version}/plspex|' \
	-e 's|"rbspex|"../ruby-%{name}-%{version}/rbspex|' \
	-e 's|"cgispex|"../%{name}-cgi-%{version}/cgispex|' \
	doc/index*.html
	
%build
## 0. First:
## - remove rpath
## - fix pc file to hide header files
## - fix Makefile to keep timestamps
for f in `find . -name Makefile.in` ; do
	%{__sed} -i.rpath -e '/^LDENV/d' $f
done
%{__sed} -i.misc \
	 -e '/^Libs/s|@LIBS@||' \
	 -e '/Cflags/s|^\(.*\)|\1 -I\${includedir}/qdbm|' \
	 qdbm.pc.in
%{__sed} -i.stamp \
	 -e 's|cp \(-R*f \)|cp -p \1| ' \
	 -e 's|^CP =.*$|CP = cp -p|' \
	`find . -name \*[mM]akefile.in -or -name \*[mM]akefile`
	 

## 1. for main
%{__sed} -i.flags -e '/^CFLAGS/s|-O3.*$|%{optflags}|' Makefile.in
%configure \
	--enable-pthread \
	--enable-zlib \
	--enable-bzip \
	--enable-iconv \
	--enable-lzo
%{__make} %{?_smp_mflags}

## 2. for C++
pushd plus
%{__sed} -i.flags -e '/^CXXFLAGS/s|@MYOPTS@|%{optflags}|' Makefile.in
%configure
%{__make} %{?_smp_mflags}
popd

## 3. for java
%ifarch %java_arches
pushd java
%{__sed} -i.flags -e '/^CFLAGS/s|@MYOPTS@|%{optflags}|' Makefile.in
export JAVA_HOME=%{java_home}
%configure
%{__make} JAR=%{jar} JAVAC=%{javac}
popd
%endif

## 4. for cgi
pushd cgi
%{__sed} -i.flags -e \
	 '/^CFLAGS/s|-O2.*$|%{optflags} -DCONFDIR="\"@sysconfdir@/qdbm/\""|' Makefile.in
%configure
%{__make} %{?_smp_mflags}
popd

## 5. for perl
pushd perl
%configure
%{__make} %{?_smp_mflags} CC="gcc %optflags" LDDLFLAGS="-shared" INSTALLDIRS=vendor
popd

## 6. for Ruby
pushd ruby
%configure
sed -i 's|extconf.rb |extconf.rb --vendor |' Makefile
%{__make} %{?_smp_mflags} CC="gcc %optflags"
popd


%install
%{__rm} -rf $RPM_BUILD_ROOT

## 1. for main
%{__make} install DESTDIR=$RPM_BUILD_ROOT

%{__rm} -rf $RPM_BUILD_ROOT%{_libdir}/lib*.a
%{__rm} -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/

## 2. for cgi
pushd cgi
%{__make} install DESTDIR=$RPM_BUILD_ROOT
popd

%{__rm} -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/cgi/*.html
%{__install} -d $RPM_BUILD_ROOT%{_sysconfdir}/qdbm

%{__mv} $RPM_BUILD_ROOT%{_datadir}/qdbm/cgi/*.conf \
	$RPM_BUILD_ROOT%{_sysconfdir}/qdbm/
rmdir $RPM_BUILD_ROOT%{_datadir}/qdbm/cgi
rmdir $RPM_BUILD_ROOT%{_datadir}/qdbm

## 3. for java
%ifarch %java_arches
pushd java
%{__make} install DESTDIR=$RPM_BUILD_ROOT JAR=%{jar}
popd

%{__mkdir_p} $RPM_BUILD_ROOT%{_jnidir}
%{__mv} -f $RPM_BUILD_ROOT%{_libdir}/*.jar \
	$RPM_BUILD_ROOT%{_jnidir}

%{__mkdir_p} $RPM_BUILD_ROOT%{_javadocdir}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/qdbm/java/japidoc \
	$RPM_BUILD_ROOT%{_javadocdir}/%{name}
%{__rm} $RPM_BUILD_ROOT%{_datadir}/qdbm/java/*.html
rmdir $RPM_BUILD_ROOT%{_datadir}/qdbm/java
rmdir $RPM_BUILD_ROOT%{_datadir}/qdbm
%endif

## 4. for perl
pushd perl
%{__make} install DESTDIR=$RPM_BUILD_ROOT INSTALLDIRS=vendor
popd

%{__rm} -rf $RPM_BUILD_ROOT%{_datadir}/qdbm/perl/plapidoc
%{__rm} $RPM_BUILD_ROOT%{_datadir}/qdbm/perl/*.html
rmdir $RPM_BUILD_ROOT%{_datadir}/qdbm/perl
rmdir $RPM_BUILD_ROOT%{_datadir}/qdbm

# Fix perl modules..
%{__rm} $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod
find $RPM_BUILD_ROOT%{perl_vendorarch} \
	-name \*.bs -or -name .packlist | \
	xargs rm -f
find $RPM_BUILD_ROOT%{perl_vendorarch} \
	-name \*.so | \
	xargs chmod 0755

## 5. for C++
pushd plus
make install DESTDIR=$RPM_BUILD_ROOT
popd

%{__rm} -rf $RPM_BUILD_ROOT%{_libdir}/lib*.a
%{__rm} -rf $RPM_BUILD_ROOT%{_datadir}/qdbm/plus/xapidoc
%{__rm} $RPM_BUILD_ROOT%{_datadir}/qdbm/plus/*.html
rmdir $RPM_BUILD_ROOT%{_datadir}/qdbm/plus
rmdir $RPM_BUILD_ROOT%{_datadir}/qdbm

## 6. for Ruby
pushd ruby
make install DESTDIR=$RPM_BUILD_ROOT
popd

%{__rm} -rf $RPM_BUILD_ROOT%{_datadir}/qdbm/ruby/rbapidoc
%{__rm} $RPM_BUILD_ROOT%{_datadir}/qdbm/ruby/*.html
rmdir $RPM_BUILD_ROOT%{_datadir}/qdbm/ruby
rmdir $RPM_BUILD_ROOT%{_datadir}/qdbm

## 7. Finally hide header files to name specific directory
pushd $RPM_BUILD_ROOT%{_includedir}
for f in *.h ; do
	for g in *.h ; do
		eval sed -i -e \'s\|include \<$g\>\|include \"$g\"\|\' $f
	done
done

%{__mkdir} qdbm
%{__mv} *.h qdbm/
popd

%ldconfig_scriptlets

%ldconfig_scriptlets java

%ldconfig_scriptlets -n qdbm++


%files
%defattr(-, root, root, -)
%doc COPYING ChangeLog NEWS README THANKS
%doc doc/*png
%doc doc/index.html
%lang(ja) %doc doc/index.ja.html

%{_bindir}/[a-wyz]*
%exclude %{_bindir}/pl*
%exclude %{_bindir}/rb*

%{_libdir}/libqdbm.so.*
# own includedir
%dir %{_includedir}/qdbm/
%{_mandir}/man1/*

%files devel
%defattr(-, root, root, -)
%doc doc/spex.html
%lang(ja) %doc doc/spex-ja.html
%{_mandir}/man3/*

%{_includedir}/qdbm/[a-w]*.h
%{_libdir}/libqdbm.so
%{_libdir}/pkgconfig/*.pc

%files cgi
%defattr(-, root, root, -)
%doc cgi/cgispex.html
%lang(ja) %doc cgi/cgispex-ja.html

%{_libexecdir}/*.cgi
%dir %{_sysconfdir}/qdbm/
%config(noreplace) %{_sysconfdir}/qdbm/*.conf

%ifarch %java_arches
%files java
%defattr(-, root, root,-)
%doc java/jspex.html
%lang(ja) %doc java/jspex-ja.html

%{_libdir}/libjqdbm.so*
%{_jnidir}/*.jar

%files javadoc
%doc %{_javadocdir}/%{name}/
%endif

%files perl
%defattr(-, root, root, -)
%doc perl/plapidoc/
%doc perl/plspex.html
%lang(ja) %doc perl/plspex-ja.html

%{_bindir}/pl*
%{perl_vendorarch}/*.pm
%{perl_vendorarch}/auto/*/

%files -n qdbm++
%defattr(-, root, root, -)

%{_bindir}/x*
%{_libdir}/libxqdbm.so.*

%files -n qdbm++-devel
%defattr(-, root, root, -)
%doc plus/xapidoc/
%doc plus/xspex.html
%lang(ja) %doc plus/xspex-ja.html

%{_includedir}/qdbm/x*.h
%{_libdir}/libxqdbm.so

%files -n ruby-qdbm
%defattr(-, root, root, -)
%doc ruby/rbapidoc/
%doc ruby/rbspex.html
%lang(ja) %doc ruby/rbspex-ja.html

%{_bindir}/rb*
%{ruby_vendorarchdir}/mod_*.so
%{ruby_vendorlibdir}/*.rb


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.78-71
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.78-70
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.78-69
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 08 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.78-68
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.4

* Fri Oct 25 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.78-67
- Reable mvn dependency generation again

* Sun Sep 29 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.78-66
- Use explicit java version for BR
- Add more BR stuff for F42
- Kill mvn dependency generator which is difficult to understand

* Sat Aug 31 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.78-65
- Explicitly specify openjdk version on F-39

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.78-64
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.78-63
- Perl 5.40 rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.78-62
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.78-61
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.78-60
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.3

* Fri Dec 29 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.78-59
- SPDX migration

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.78-58
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.78-57
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.78-56
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 04 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.78-55
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.2

* Fri Nov 25 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.78-54
- Patch for ruby module for c99 conformant: -Werror=implicit-int

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.78-53
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jul  9 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.78-52
- Adopt %%java_arches https://fedoraproject.org/wiki/Changes/Drop_i686_JDKs

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.78-51
- Perl 5.36 rebuild

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1.8.78-50
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 27 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.78-49
- F-36: rebuild against ruby31

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.78-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Dec  5 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.78-47
- Patch for java 13 / 17 yield keyword change

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.78-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.78-45
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.78-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 07 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.78-43
- F-34: rebuild against ruby 3.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.78-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 1.8.78-41
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.78-40
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.78-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.78-38
- F-32: rebuild against ruby27

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.78-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.78-36
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.78-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.78-34
- F-30: rebuild against ruby26

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.78-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.78-32
- Perl 5.28 rebuild

* Mon Jun 18 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.78-31
- F-29: BR javapackages-tools for java rpm macros (bug 1591153)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.78-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 03 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.78-29
- F-28: rebuild for ruby25

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.78-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.78-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.78-26
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.78-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 11 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.78-24
- F-26: rebuild for ruby24

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.78-23
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.78-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 13 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.78-21
- F-24: rebuild against ruby23

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.78-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.78-19
- Perl 5.22 rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.8.78-18
- Rebuilt for GCC 5 C++11 ABI change

* Fri Jan 16 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.78-17
- F-22: rebuild for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.78-16
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.78-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 16 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 1.8.78-14
- Re-enable Java bindings using openjdk
- Move jar to %%_jnidir and javadocs to %%_javadocdir
- Add javadoc package per current Java packaging guidelines

* Thu Jun 12 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.78-13
- F-21: disable java due to gcc-java vanishment

* Mon Apr 28 2014 Vít Ondruch <vondruch@redhat.com> - 1.8.78-12
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.78-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.8.78-10
- Perl 5.18 rebuild

* Sun Mar 17 2013 Mamour TASAKA <mtasaka@fedoraproject.org> - 1.8.78-9
- F-19: rebuild for ruby 2.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.78-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.78-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1.8.78-6
- Perl 5.16 rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.78-5
- Rebuilt for c++ ABI breakage

* Wed Feb 08 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.8.78-4
- Rebuilt for Ruby 1.9.3.

* Thu Jan  5 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.8.78-3
- F-17: rebuild against gcc47

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.8.78-2
- Perl mass rebuild

* Fri Aug 27 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.78-1
- 1.8.78

* Wed Jun 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.8.77-7
- Mass rebuild with perl-5.12.0

* Wed Dec 23 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.77-6
- F-13: rebuild for new perl

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.77-5
- F-12: Mass rebuild

* Tue Feb 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.77-4
- F-11: Mass rebuild

* Fri Mar 14 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.77-3
- Support LZO compression (thanks to Karsten Hopp)
- And rebuild against new perl (F-9)

* Sat Feb  9 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Rebuild against gcc43 (F-9)

* Sat Nov 17 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.77-1
- 1.8.77

* Sun Nov  4 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.76-1
- 1.8.76

* Wed Aug 22 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.75-3.dist.2
- Mass rebuild (buildID or binutils issue)

* Fri Aug  3 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.75-3.dist.1
- License update

* Thu Jun 16 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.75-3
- Fix java directory

* Thu Mar 22 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.75-1
- 1.8.75
- Ruby subpackage description change according to Guildlines

* Thu Mar  8 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.74-3
- Add JAVAC direction and perl-devel for BR

* Fri Feb 23 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.74-2
- Add missing release dependency
- Change group from Development to System Environment
- Remove duplicate files and fix the dependency for main package.

* Wed Feb 21 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.74-1
- Rewrite.

* Tue Sep 12 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.70-1
- Initial package.

