# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name: xmlstarlet
Version: 1.6.1
Release: 28%{?dist}
Summary: Command Line XML Toolkit
License: MIT
URL: http://xmlstar.sourceforge.net/
Source0: http://downloads.sourceforge.net/xmlstar/%{name}-%{version}.tar.gz
# https://sourceforge.net/p/xmlstar/bugs/109/
Patch0: xmlstarlet-1.6.1-nogit.patch
# http://sourceforge.net/tracker/?func=detail&aid=3266898&group_id=66612&atid=515106

BuildRequires: make
BuildRequires: gcc
BuildRequires: xmlto automake autoconf libxslt-devel
BuildRequires: libxml2-devel >= 2.6.23


%description
XMLStarlet is a set of command line utilities which can be used
to transform, query, validate, and edit XML documents and files
using simple set of shell commands in similar way it is done for
plain text files using UNIX grep, sed, awk, diff, patch, join, etc
commands.

%prep
%autosetup -p1


%build
autoreconf -i
%configure --disable-static-libs --with-libxml-include-prefix=%{_includedir}/libxml2 --docdir=%{_pkgdocdir} # --libdir=%{_libdir}
%make_build


%install
%make_install
# Avoid name kludging in autotools
mv %{buildroot}%{_bindir}/xml %{buildroot}%{_bindir}/xmlstarlet


%check
make check



%files
%doc AUTHORS ChangeLog NEWS README Copyright TODO
%doc %{_pkgdocdir}/*
%{_mandir}/man1/xmlstarlet.1*
%{_bindir}/xmlstarlet


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Nov 29 2024 Paul W. Frields <stickster@gmail.com> - 1.6.1-26
- Remove docbook5-schemas BR due to deprecation

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 05 2023 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.6.1-22
- SPDX migration

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Mar 17 2022 Neal Gompa <ngompa@datto.com> - 1.6.1-19
- Minor spec improvements

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Mar 01 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 1.6.1-6
- Mark installed documentation as %%doc (#1308255)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Dec  8 2014 Paul W. Frields <stickster@gmail.com> - 1.6.1-3
- Fix noisy git related spew (#1171864)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Paul W. Frields <stickster@gmail.com> - 1.6.1-1
- Update to upstream 1.6.1 (#1129106)

* Mon Jun 16 2014 Paul W. Frields <stickster@gmail.com> - 1.6.0-1
- Update to upstream 1.6.0 (#1037400, #1107292)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Jul 27 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.5.0-2
- Install docs to %%{_pkgdocdir} where available.

* Wed Jul 10 2013 Paul W. Frields <stickster@gmail.com> - 1.5.0-1
- Update to upstream 1.5.0 (#983025)
- Fix man page rendering (#981050)
- Use standard docdir

* Mon Mar 25 2013 Paul W. Frields <stickster@gmail.com> - 1.4.2-1
- Update to upstream 1.4.2 (#851880)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 15 2012 Paul W. Frields <stickster@gmail.com> - 1.3.1-2
- Fix build with configure flag

* Wed Feb 15 2012 Paul W. Frields <stickster@gmail.com> - 1.3.1-1
- Update to upstream 1.3.1 (#782066)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct  3 2011 Paul W. Frields <stickster@gmail.com> - 1.3.0-1
- Update to upstream 1.3.0

* Fri Aug 26 2011 Paul W. Frields <stickster@gmail.com> - 1.2.1-1
- Update to upstream 1.2.1

* Sun Apr 10 2011 Paul W. Frields <stickster@gmail.com> - 1.1.0-1
- Update to upstream 1.1.0

* Thu Apr 07 2011 Dan Horák <dan[at]danny.cz> - 1.0.6-2
- fix build on 64-bit big-endians

* Sat Mar 26 2011 Paul W. Frields <stickster@gmail.com> - 1.0.6-1
- Update to upstream 1.0.6
- Drop obsolete patch

* Thu Feb 17 2011 Paul W. Frields <stickster@gmail.com> - 1.0.5-1
- Update to upstream 1.0.5
- Update libxml2 requirement
- Drop unnecessary patch, naming issue fixed upstream

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Paul W. Frields <stickster@gmail.com> - 1.0.4-1
- Update to new upstream 1.0.4
- Drop patches for fixed upstream issues

* Fri Dec 17 2010 Paul W. Frields <stickster@gmail.com> - 1.0.3-1
- Update to new upstream 1.0.3
- Add %%check section for validation testing

* Mon Nov  1 2010 Paul W. Frields <stickster@gmail.com> - 1.0.2-1
- Update to new upstream 1.0.2

* Sun Jan 10 2010 Paul W. Frields <stickster@gmail.com> - 1.0.1-9
- Correct source URL

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Mar 21 2008 Paul W. Frields <stickster@gmail.com> - 1.0.1-6
- Rebuild to use FORTIFY_SOURCE correctly

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.1-5
- Autorebuild for GCC 4.3

* Sat Sep  2 2006 Paul W. Frields <stickster@gmail.com> - 1.0.1-4
- Bump release for FC6 mass rebuild

* Fri Feb 17 2006 Paul W. Frields <stickster@gmail.com> - 1.0.1-3
- FESCo mandated rebuild

* Wed Nov 23 2005 Paul W. Frields <stickster@gmail.com> - 1.0.1-2
- Minor changes per review

* Tue Nov 22 2005 Paul W. Frields <stickster@gmail.com> - 1.0.1-1.2
- Improve patching to conquer inconsistent naming

* Tue Nov 22 2005 Paul W. Frields <stickster@gmail.com> - 1.0.1-1.1
- Initial RPM version


