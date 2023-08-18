Summary:        Validating XML Parser
Name:           xerces-c
Version:        3.2.4
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://xml.apache.org/xerces-c/
Source:         https://downloads.apache.org/xerces/c/3/sources/xerces-c-%{version}.tar.xz
BuildRequires:  dos2unix
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Xerces-C is a validating XML parser written in a portable
subset of C++. Xerces-C makes it easy to give your application the
ability to read and write XML data. A shared library is provided for
parsing, generating, manipulating, and validating XML
documents. Xerces-C is faithful to the XML 1.0 recommendation and
associated standards: XML 1.0 (Third Edition), XML 1.1 (First
Edition), DOM Level 1, 2, 3 Core, DOM Level 2.0 Traversal and Range,
DOM Level 3.0 Load and Save, SAX 1.0 and SAX 2.0, Namespaces in XML,
Namespaces in XML 1.1, XML Schema, XML Inclusions).

%package	devel
Summary:        Header files, libraries and development documentation for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%package doc
Summary:        Documentation for Xerces-C++ validating XML parser
BuildArch:      noarch

%description doc
Documentation for Xerces-C++.

Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.

%prep
%setup -q
# Copy samples before build to avoid including built binaries in -doc package
mkdir -p _docs
cp -a samples/ _docs/

%build
# --disable-sse2 makes sure explicit -msse2 isn't passed to gcc so
# the binaries would be compatible with non-SSE2 i686 hardware.
# This only affects i686, as on x86_64 the compiler uses SSE2 by default.
export CFLAGS="%{optflags} -fno-strict-aliasing"
export CXXFLAGS="$CFLAGS"
%configure --disable-static \
  --disable-sse2
%make_build V=1

%install
%make_install
# Correct errors in encoding
iconv -f iso8859-1 -t utf-8 CREDITS > CREDITS.tmp && mv -f CREDITS.tmp CREDITS
# Correct errors in line endings
pushd doc; dos2unix -k *.xml; popd
# Remove unwanted binaries
rm -rf %{buildroot}%{_bindir}
# Remove .la files
find %{buildroot} -type f -name "*.la" -delete -print

%check
# no upstream unit tests yet

%files
%license LICENSE
%{_libdir}/libxerces-c-3.2.so

%files devel
%{_libdir}/libxerces-c.so
%{_libdir}/pkgconfig/xerces-c.pc
%{_includedir}/xercesc/

%files doc
%license LICENSE
%doc README NOTICE CREDITS doc _docs/*

%changelog
* Thu Aug 10 2023 Saranya R <rsaranya@microsoft.com> - 3.2.4-1
- Initial CBL-Mariner import from Fedora 38 (license: MIT).
- License verified

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 07 2022 Antonio Trande <sagitter@fedoraproject.org> - 3.2.3-5
- Rebuild for EPEL9

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Apr 10 2020 Kalev Lember <klember@redhat.com> - 3.2.3-1
- Update to 3.2.3

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 03 2018 Kalev Lember <klember@redhat.com> - 3.2.2-1
- Update to 3.2.2

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 Kalev Lember <klember@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Tue Feb 06 2018 Pete Walter <pwalter@fedoraproject.org> - 3.2.0-1
- Update to 3.2.0
- Spec cleanup

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jun 30 2016 Kalev Lember <klember@redhat.com> - 3.1.4-1
- Update to 3.1.4, fixing CVE-2016-2099 and CVE-2016-4463

* Thu Apr 07 2016 Kalev Lember <klember@redhat.com> - 3.1.3-1
- Update to 3.1.3, fixing CVE-2016-0729

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.1.2-2
- Rebuilt for GCC 5 C++11 ABI change

* Fri Mar 20 2015 Kalev Lember <kalevlember@gmail.com> - 3.1.2-1
- Update to 3.1.2, fixing CVE-2015-0252
- Tighten -devel deps with the _isa macro
- Use the license macro for the LICENSE file

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Mar 09 2011 Kalev Lember <kalev@smartlink.ee> - 3.1.1-1
- Update to 3.1.1
- Dropped CVE-2009-1885 patch.
- Use dos2unix -k instead of unrecognized option -U
- Removed the multilib conflict workaround as Xerces_autoconf_config.hpp
  no longer contains the conflicting XERCES_SIZEOF_LONG define.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul  9 2010 Jonathan Robie <jrobie@localhost.localdomain> - 3.0.1-20
- Added no-strict-aliasing flag to stop rpmdiff from griping

* Wed May 26 2010 Kalev Lember <kalev@smartlink.ee> 3.0.1-19
- Fix multilib conflict caused by Xerces_autoconf_config.hpp (#595923)

* Fri May 14 2010 Kalev Lember <kalev@smartlink.ee> 3.0.1-18
- Build -doc subpackage as noarch

* Fri May 14 2010 Kalev Lember <kalev@smartlink.ee> 3.0.1-17
- Disable explicit -msse2 to make sure the binaries run on non-SSE2 i686

* Sun Feb 07 2010 Kalev Lember <kalev@smartlink.ee> 3.0.1-16
- Reintroduce a patch for CVE-2009-1885
- Don't build static library
- Use parallel make
- Spec file clean up

* Thu Feb 4 2010 Jonathan Robie <jonathan.robie@redhat.com> 3.0.1-15
- Corrected .spec file

* Wed Feb 3 2010 Jonathan Robie <jonathan.robie@redhat.com> 3.0.1-1
- Move to Xerces 3.0.1.

* Thu Aug  6 2009 Peter Lemenkov <lemenkov@gmail.com> 2.8.0-5
- Fix CVE-2009-1885

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jun 30 2008 Peter Lemenkov <lemenkov@gmail.com> 2.8.0-2
- Spec cleanups ( https://bugzilla.redhat.com/show_bug.cgi?id=435132 )

* Sun Feb 10 2008 Peter Lemenkov <lemenkov@gmail.com> 2.8.0-1
- Ver. 2.8.0

* Sat Nov 25 2006 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-6
- typo fix

* Sat Nov 25 2006 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-5
- fixed some rpmlint warnings

* Fri Nov 24 2006 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-4
- Added samples to docs-package

* Sat Nov 18 2006 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-3
- improvements suggested by Aurelien Bompard

* Sat Oct 14 2006 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-2
- Disabled package 'samples'

* Fri Oct 13 2006 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-1
- initial build for FE

* Fri Jan 06 2006 Dag Wieers <dag@wieers.com> - 2.7.0-1 - 3891/dag
- Cleaned SPEC file.

* Tue Jan 03 2006 Dries Verachtert <dries@ulyssis.org> - 2.7.0-1
- Updated to release 2.7.0.

* Thu Sep 22 2005 C.Lee Taylor <leet@leenx.co.za> 2.6.1-1
- Update to 2.6.1
- Build for FC4 32/64bit

* Sat Aug 20 2005 Che
- initial rpm release
