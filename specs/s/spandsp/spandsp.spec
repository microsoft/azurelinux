# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#global pre 21

Name:           spandsp
Summary:        A DSP library for telephony
Version:        0.0.6
Release:        21%{?pre:.pre%{pre}}%{?dist}
License:        LGPL-2.1-only AND GPL-2.0-only
URL:            https://www.soft-switch.org
# Remove non-free file (no permission to redistribute)
# rm -rf spandsp-0.0.6/test-data/local/lenna-colour.tif
# Source:         %{url}/downloads/spandsp/spandsp-%{version}%{?pre:pre%{pre}}.tar.gz
Source0:	spandsp-%{version}%{?pre:pre%{pre}}-clean.tar.gz

BuildRequires: make
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool

BuildRequires:  gcc

BuildRequires:  libxml2-devel
BuildRequires:  libtiff-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  doxygen
BuildRequires:  libxslt
BuildRequires:  docbook-style-xsl

%description
SpanDSP is a library of DSP functions for telephony, in the 8000
sample per second world of E1s, T1s, and higher order PCM channels. It
contains low level functions, such as basic filters. It also contains
higher level functions, such as cadenced supervisory tone detection,
and a complete software FAX machine. The software has been designed to
avoid intellectual property issues, using mature techniques where all
relevant patents have expired. See the file DueDiligence for important
information about these intellectual property issues.

%package devel
Summary:        SpanDSP development files
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       libtiff-devel%{?_isa}

%description devel
%{summary}.

%package apidoc
Summary:        SpanDSP API documentation

%description apidoc
%{summary}.

%prep
%autosetup

%build
autoreconf -f -v -i
%configure --enable-doc --disable-static --disable-rpath
%make_build
find doc/api -type f | xargs touch -r configure

%install
%make_install
rm -vf %{buildroot}%{_libdir}/*.la
mkdir -p %{buildroot}%{_datadir}/%{name}

%ldconfig_scriptlets

%files
%license COPYING
%doc DueDiligence ChangeLog AUTHORS NEWS README
%{_libdir}/lib%{name}.so.*
%{_datadir}/%{name}/

%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%files apidoc
%doc doc/api/html/*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 28 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.0.6-1
- Update to 0.0.6

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-0.15.pre21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.6-0.14.pre21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.6-0.13.pre21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.6-0.12.pre21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.6-0.11.pre21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 27 2013 Jeffrey Ollie <jeff@ocjtech.us> - 0.0.6-0.10.pre21
- Run autoreconf to pick up aarch64 support. #926560

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.6-0.9.pre21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 18 2012 Jeffrey Ollie <jeff@ocjtech.us> - 0.0.6-0.8.pre21
- Update to 0.0.6pre21

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.6-0.7.pre18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.6-0.6.pre18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 27 2011 Rex Dieter <rdieter@fedoraproject.org> 0.0.6-0.5.pre18
- use of brackets confuses autotools (#691039)

* Wed Feb  9 2011 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.6-0.4.pre18
- 0.0.6pre18

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.6-0.3.pre17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Aug  1 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.6-0.2.pre17
- Update to 0.0.6pre17

* Tue Jul 28 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.6-0.1.pre12
- Update to 0.0.6pre12

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.5-0.3.pre4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.5-0.2.pre4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul 30 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.5-0.1.pre4
- Update to 0.0.5pre4

* Thu Mar 20 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.10.pre18
- Update to 0.0.4pre18

* Mon Feb 11 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.9.pre16
- Rebuild for GCC 4.3

* Fri Nov 30 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.8.pre16
- Fix release version

* Fri Nov 30 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.8.pre16
- Update to 0.0.4pre16

* Thu Nov  1 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.7.pre15
- Update to 0.0.4pre15

* Thu Nov  1 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.6.pre11
- Try and fix multilib problems with generated API docs.

* Fri Oct 26 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.5.pre11
- Update to 0.0.4pre11

* Fri Sep  7 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.4.pre8
- Update to 0.0.4pre8

* Sat Aug 25 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.2.pre7
- Update to 0.0.4pre7

* Wed Aug 22 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.1.pre6
- Bump release because I forgot to upload new sources...

* Wed Aug 22 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.1.pre6
- Update to 0.0.4pre6
- Update license tag.

* Wed Aug  8 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.1.pre4
- Update to 0.0.4pre4

* Mon Jun 11 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.4-0.1.pre3
- Update to 0.0.4pre3

* Fri Apr 13 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.3-3
- Fix usage of dist macro, pointed out by dgilmore

* Mon Apr  9 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.3-2
- Update to final 0.0.3.

* Tue Mar  6 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.3-1.pre28
- Update to 0.0.3pre28

* Mon Dec 11 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.3-1.pre27
- Update to 0.0.3pre27

* Tue Nov 21 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.3-1.pre25
- Update to 0.0.3pre25

* Sat Oct  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.3-1.pre24
- Update to 0.0.3pre24
- Add dist tag.

* Thu Oct  5 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.3-1.pre23
- Update to 0.0.3pre23

* Thu Oct  5 2006 David Woodhouse <dwmw2@infradead.org> - 0.0.2-1.pre26
- Update to 0.0.2pre26

* Mon Mar  6 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0.2-1.pre25
- "Downgrade" to 0.0.2pre25 - 0.0.3 does not work with Asterisk.
- Don't use dos2unix, use sed.

* Mon Nov 14 2005 Jeffrey C. Ollie <jcollie@lt16585.campus.dmacc.edu> - 0.0.3-0.3.pre6
- Update to 0.0.3pre6

* Mon Oct 24 2005 Jeffrey C. Ollie <jcollie@lt16585.campus.dmacc.edu> - 0.0.3-0.2.pre4
- Changed Source0 to Source
- Changed setup0 to setup
- Added COPYING to doc in main package.
- Removed html API docs from main package.

* Tue Oct 18 2005 Jeffrey C. Ollie <jcollie@lt16585.campus.dmacc.edu> - 0.0.3-0.1.pre4
- Initial build.

