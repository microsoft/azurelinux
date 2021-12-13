Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:		dotconf
Version:	1.3
Release:	24%{?dist}
Summary:	Libraries to parse configuration files
License:	LGPLv2
URL:		https://github.com/williamh/dotconf/
Source:		%{name}-%{version}.tar.gz
 
BuildRequires:	findutils
BuildRequires:	gcc
BuildRequires:	glibc-common
BuildRequires:	make

%description
Dotconf is a library used to handle configuration files.

%package	devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconf-pkg-config


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"

iconv -f iso-8859-2 -t utf-8 -o iconv.tmp AUTHORS
mv iconv.tmp AUTHORS
iconv -f iso-8859-2 -t utf-8 -o iconv.tmp doc/dotconf-features.txt
mv iconv.tmp doc/dotconf-features.txt
rm examples/maketest.sh
find %{buildroot} -type f -name "*.a" -o -name "*.la" | xargs rm -f

# move installed docs to include them in -devel package via %%doc magic
rm -rf __tmp_doc ; mkdir __tmp_doc
mv ${RPM_BUILD_ROOT}%{_docdir}/%{name}/* __tmp_doc

%ldconfig_scriptlets

%files
%license COPYING
%doc README AUTHORS
%{_libdir}/libdotconf*.so.*

%files devel
%doc __tmp_doc/*
%{_libdir}/libdotconf*.so
%{_includedir}/dotconf.h
%{_libdir}/pkgconfig/dotconf.pc

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3-24
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Sep 13 2019 Wim Taymans <wtaymans@redhat.com> - 1.3-22
- Fix URL

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar  7 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.3-18
- Modernise spec, add BR gcc

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3-16
- Switch to %%ldconfig_scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 14 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3-8
- Fix duplicate documentation (#1001258) by using only %%doc magic
- pkgconfig dep is automatic
- Use %%?_isa in -devel base package dep

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.3-6
- Fix multilib issues (thanks Rui Matos)

* Tue Feb  5 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.3-5
- Update URLs and note github SCV url

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec  8 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.3-1
- New upstream 1.3 release, update URL/Source

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 03 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.0.13-7
- Override config.{sub,guess} explicitly due to redhat-rpm-build-config
  behavior change on F-10+, otherwise build fails on ppc64

* Sun Mar 09 2008 Assim Deodia<assim.deodia@gmail.com> 1.0.13-6
- fixed m4-underquote error

* Fri Feb 29 2008 Assim Deodia<assim.deodia@gmail.com> 1.0.13-5
- fixed AUTHORS utf-8
- fixed doc/dotconf-features.txt utf-8

* Sat Feb 23 2008 Assim Deodia<assim.deodia@gmail.com> 1.0.13-4
- Applied patch macro

* Sat Feb 23 2008 Assim Deodia<assim.deodia@gmail.com> 1.0.13-3
- Resolved Multilib issue

* Fri Feb 22 2008 Assim Deodia<assim.deodia@gmail.com> 1.0.13-2
- Inclusion of pkgconfig
- Removal of INSTALL file
- Proper placement of Library files
- Creating devel sub-package
- Chaning source URL

* Sun Feb 17 2008 Assim Deodia<assim.deodia@gmail.com> 1.0.13-1
- Initial Commit
