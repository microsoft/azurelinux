# spec file for mcpp / compiler-independent-library-build on fedora
Summary:        Alternative C/C++ preprocessor
Name:           mcpp
Version:        2.7.2
Release:        28%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://mcpp.sourceforge.net/
Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:         mcpp-manual.html.patch
# Extracted from http://www.zeroc.com/download/Ice/3.4/ThirdParty-Sources-3.4.2.tar.gz
# Also responsible for fixing CVE-2019-14274
Patch1:         patch.mcpp.2.7.2
# https://bugzilla.redhat.com/show_bug.cgi?id=948860
Patch2:         mcpp-man.patch
BuildRequires:  gcc

%description
C/C++ preprocessor defines and expands macros and processes '#if',
'#include' and some other directives.

MCPP is an alternative C/C++ preprocessor with the highest conformance.
It supports multiple standards: K&R, ISO C90, ISO C99, and ISO C++98.
MCPP is especially useful for debugging a source program which uses
complicated macros and also useful for checking portability of a source.

Though mcpp could be built as a replacement of GCC's resident
preprocessor or as a stand-alone program without using library build of
mcpp, this package installs only a program named 'mcpp' which links
shared library of mcpp and behaves independent from GCC.

%package -n     libmcpp
Summary:        Alternative C/C++ preprocessor (library build)

%description -n libmcpp
This package provides a library build of mcpp.

%package -n     libmcpp-devel
Summary:        Alternative C/C++ preprocessor (development package for library build)
Requires:       libmcpp = %{version}-%{release}

%description -n libmcpp-devel
Development package for libmcpp.

%package        doc
Summary:        Alternative C/C++ preprocessor (manual for library build)

%description doc
This package provides an html manual for mcpp.

%prep
%setup -q
%patch0 -b -z.euc-jp
%patch1 -p1
%patch2 -p1

%build
%configure --enable-mcpplib --disable-static
%make_build
mv mcpp-gcc.1 mcpp.1

%install
iconv -f euc-jp -t utf-8 doc-jp/mcpp-manual.html > doc-jp/mcpp-manual-jp.html
%make_install
rm -rf %{buildroot}%{_docdir}/%{name}
rm -f %{buildroot}%{_libdir}/libmcpp.la

%ldconfig_scriptlets -n libmcpp

%files
%license LICENSE
%doc ChangeLog ChangeLog.old NEWS README
%{_mandir}/man1/%{name}.1*
%{_bindir}/%{name}

%files -n libmcpp
%license LICENSE
%{_libdir}/libmcpp.so.*

%files -n libmcpp-devel
%{_libdir}/libmcpp.so
%{_includedir}/mcpp_lib.h
%{_includedir}/mcpp_out.h

%files doc
%license LICENSE doc-jp/LICENSE
%doc doc/mcpp-manual.html
%lang(ja) %doc doc-jp/mcpp-manual-jp.html

%changelog
* Mon Jun 27 2022 Daniel McIlvaney <damcilva@microsoft.com> - 2.7.2-28
- Add inline comments to patch.mcpp.2.7.2 patch file to indicate it fixes CVE-2019-14274.

* Wed Dec 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.7.2-27
- License verified
- Lint spec
- Fixed libmcpp-devel requires

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.7.2-26
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.2-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.2-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 18 2018 Owen Taylor <otaylor@redhat.com> - 2.7.2-22
- Handle both compressed and uncompressed manual pages

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.7.2-14
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 20 2013 Petr Machata <pmachata@redhat.com> - 2.7.2-10
- Update usage output and man pages to include some omited options.
  (mcpp-man.patch)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 16 2011 Mary Ellen Foster <mefoster at gmail.com> - 2.7.2-6
- Update upstream Ice patch to latest version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 Kiyoshi Matsui <kmatsui@t3.rim.or.jp> 2.7.2-4
- Make subpackages to include LICENSE.

* Tue Oct 13 2009 Mary Ellen Foster <mefoster at gmail.com>
- Incorporate patch from Ice upstream project

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 01 2008 Kiyoshi Matsui <kmatsui@t3.rim.or.jp> 2.7.2-1
- Upstream new release.

* Tue May 20 2008 Kiyoshi Matsui <kmatsui@t3.rim.or.jp> 2.7.1-1
- Upstream new release.
- Change to library build.
- Devide to 4 packages: mcpp, libmcpp, libmcpp-devel and mcpp-doc.
- Thanks to Mary Ellen Foster for correcting this spec file.

* Sun Mar 24 2008 Kiyoshi Matsui <kmatsui@t3.rim.or.jp> 2.7-2
- Upstream new release.

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.6.4-2
- Rebuild for selinux ppc32 issue.

* Thu May 19 2007 Kiyoshi Matsui <kmatsui@t3.rim.or.jp> 2.6.4-1
- Upstream new release.

* Fri Apr 27 2007 Kiyoshi Matsui <kmatsui@t3.rim.or.jp> 2.6.3-5
- Apply the new patch (patch1) for mcpp.

* Wed Apr 25 2007 Kiyoshi Matsui <kmatsui@t3.rim.or.jp> 2.6.3-4
- Change installation of doc/mcpp-manual.html and doc-jp/mcpp-manual.html.

* Tue Apr 24 2007 Kiyoshi Matsui <kmatsui@t3.rim.or.jp> 2.6.3-3
- Revise many points to adapt to the guideline of Fedora (thanks to
        the review by Mamoru Tasaka):
    use %%dist, %%configure, %%optflags, %%{_datadir}, %%lang(ja),
    convert encoding of mcpp-manual.html to utf-8,
    and others.

* Sat Apr 21 2007 Kiyoshi Matsui <kmatsui@t3.rim.or.jp> 2.6.3-2
- Replace some variables with macros.
- Rename this spec file.

* Sat Apr 07 2007 Kiyoshi Matsui <kmatsui@t3.rim.or.jp> 2.6.3-1
- First release for V.2.6.3 on sourceforge.
