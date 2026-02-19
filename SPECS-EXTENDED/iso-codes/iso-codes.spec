Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           iso-codes
Summary:        ISO code lists and translations
Version:        4.17.0
Release:        1%{?dist}
License:        LGPL-2.1-or-later
URL:            https://salsa.debian.org/iso-codes-team/iso-codes
Source0:        https://salsa.debian.org/iso-codes-team/%{name}/-/archive/v%{version}/%{name}-v%{version}.tar.gz

BuildRequires:  gettext
BuildRequires:  python3
BuildRequires:  make
BuildArch:      noarch

# for /usr/share/xml
Requires:       xml-common

%description
This package provides the ISO 639 Language code list, the ISO 4217
Currency code list, the ISO 3166 Territory code list, and ISO 3166-2
sub-territory lists, and all their translations in gettext format.

%package devel
Summary:        Files for development using %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains the pkg-config files for development
when building programs that use %{name}.

%prep
%autosetup -n %{name}-v%{version}

# The '&' character is not getting parsed using xmllint
# Change it to "and" word
sed -i 's/ & / and /g' data/iso_3166-2.json

%build
%configure
%make_build

%install
%make_install INSTALL="%{__install} -p"

%find_lang %{name} --all-name

%files -f %{name}.lang
%doc CHANGELOG.md README.md
%license COPYING
%dir %{_datadir}/xml/iso-codes
%{_datadir}/xml/iso-codes/*.xml
%{_datadir}/iso-codes

%files devel
%{_datadir}/pkgconfig/iso-codes.pc


%changelog
* Wed oct 23 2024 Akarsh Chaudhary <v-akarshc@microsoft.com> - 4.17.0-1
- Update to version 4.17.0

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.4-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 09 2019 Parag Nemade <pnemade AT redhat DOT com> - 4.4-1
- Update to 4.4 version (#1758138)

* Fri Aug 16 2019 Parag Nemade <pnemade AT redhat DOT com> - 4.3-2
- Simple rebuilt to have f32 and f31 dist-git in sync

* Fri Aug 16 2019 Parag Nemade <pnemade AT redhat DOT com> - 4.3-1
- Update to 4.3 version (#1733770)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Parag Nemade <pnemade AT redhat DOT com> - 4.2-1
- Update to 4.2 version (#1669653)

* Fri Dec 14 2018 Parag Nemade <pnemade AT redhat DOT com> - 4.1-1
- Update to 4.1 version (#1659319)
- Upstream moved ChangeLog to ChangeLog.md

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.79-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 16 2018 Parag Nemade <pnemade AT redhat DOT com> - 3.79-1
- Update to 3.79 version (#1577820)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.77-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 22 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.77-1
- Update to 3.77 version (#1516284)

* Tue Sep 19 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.76-1
- Update to 3.76 version

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.75-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Apr 26 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.75-1
- Update to 3.75 version

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.74-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 19 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.74-1
- Update to 3.74

* Tue Jan 03 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.73-1
- Update to 3.73

* Mon Jan 02 2017 Björn Esser <bjoern.esser@gmail.com> - 3.72-2
- Updated spec to use recent macros
- Added needed BR: python3

* Mon Dec 12 2016 Parag Nemade <pnemade AT redhat DOT com> - 3.72-1
- Update to 3.72

* Thu Nov 17 2016 Parag Nemade <pnemade AT redhat DOT com> - 3.71-1
- Update to 3.71

* Tue Aug 30 2016 Parag Nemade <pnemade AT redhat DOT com> - 3.70-1
- Update to 3.70

* Mon Aug 08 2016 Parag Nemade <pnemade AT redhat DOT com> - 3.69-1
- Update to 3.69

* Tue May 03 2016 Parag Nemade <pnemade AT redhat DOT com> - 3.68-1
- Upstream renamed README to README.md
- Update to 3.68

* Mon Apr 04 2016 Parag Nemade <pnemade AT redhat DOT com> - 3.67-1
- Update to 3.67
- LICENSE renamed to COPYING file

* Wed Mar 02 2016 Parag Nemade <pnemade AT redhat DOT com> - 3.66-1
- Update to 3.66
- Upstream now providing json formatted iso-codes data

* Thu Feb 04 2016 Parag Nemade <pnemade AT redhat DOT com> - 3.65-1
- Update to 3.65

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.64-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 05 2016 Parag Nemade <pnemade AT redhat DOT com> - 3.64-1
- Update to 3.64

* Fri Nov 27 2015 Parag Nemade <pnemade AT redhat DOT com> - 3.63-1
- Update to 3.63

* Fri Oct 02 2015 Parag Nemade <pnemade AT redhat DOT com> - 3.62-1
- Update to 3.62

* Wed Sep 02 2015 Parag Nemade <pnemade AT redhat DOT com> - 3.61-1
- Update to 3.61
- Drop Group tag
- use %%license macro

* Mon Aug 03 2015 Parag Nemade <pnemade AT redhat DOT com> - 3.60-1
- Update to 3.60

* Fri Jul 03 2015 Parag Nemade <pnemade AT redhat DOT com> - 3.59-1
- Update to 3.59

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.58-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 09 2015 Parag Nemade <pnemade AT redhat DOT com> - 3.58-1
- Update to 3.58

* Tue Oct 28 2014 Parag Nemade <pnemade AT redhat DOT com> - 3.57-1
- Update to 3.57

* Wed Sep 03 2014 Parag Nemade <pnemade AT redhat DOT com> - 3.56-1
- Update to 3.56

* Thu Jul 10 2014 Parag Nemade <pnemade AT redhat DOT com> - 3.55-1
- Update to 3.55

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Parag Nemade <pnemade AT redhat DOT com> - 3.54-1
- Update to 3.54

* Fri May 02 2014 Parag Nemade <pnemade AT redhat DOT com> - 3.53-1
- Update to 3.53

* Thu Apr 03 2014 Parag Nemade <pnemade AT redhat DOT com> - 3.52-1
- Update to 3.52

* Tue Feb 04 2014 Parag Nemade <pnemade AT redhat DOT com> - 3.51-1
- Update to 3.51

* Thu Jan 02 2014 Parag Nemade <pnemade AT redhat DOT com> - 3.50-1
- Update to 3.50

* Fri Dec 06 2013 Parag Nemade <pnemade AT redhat DOT com> - 3.49-1
- Update to 3.49

* Sun Nov 03 2013 Parag Nemade <pnemade AT redhat DOT com> - 3.48-1
- Update to 3.48

* Fri Oct 04 2013 Parag Nemade <pnemade AT redhat DOT com> - 3.47-1
- Update to 3.47

* Mon Sep 02 2013 Parag Nemade <pnemade AT redhat DOT com> - 3.46-1
- Update to 3.46

* Mon Aug 05 2013 Parag Nemade <pnemade AT redhat DOT com> - 3.45-1
- Update to 3.45

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 05 2013 Parag Nemade <pnemade AT redhat DOT com> - 3.44-1
- Update to 3.44

* Mon Jun 10 2013 Parag Nemade <pnemade AT redhat DOT com> - 3.43-1
- Update to 3.43

* Tue May 07 2013 Parag Nemade <pnemade AT redhat DOT com> - 3.42-1
- Update to 3.42

* Wed Feb 27 2013 Parag Nemade <pnemade AT redhat DOT com> - 3.41-2
- bump the spec for missing updated sources

* Mon Feb 25 2013 Parag Nemade <pnemade AT redhat DOT com> - 3.41-1
- Update to 3.41

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Nov 04 2012 Parag Nemade <pnemade AT redhat DOT com> - 3.40-1
- Update to 3.40

* Thu Oct 04 2012 Parag Nemade <pnemade AT redhat DOT com> - 3.39-1
- Update to 3.39

* Wed Aug 08 2012 Parag Nemade <pnemade AT redhat DOT com> - 3.38-1
- Update to 3.38

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 02 2012 Parag Nemade <pnemade AT redhat DOT com> - 3.37-1
- Update to 3.37

* Thu Jun 07 2012 Parag Nemade <pnemade AT redhat DOT com> - 3.36-1
- Update to 3.36

* Wed May 02 2012 Parag Nemade <pnemade AT redhat DOT com> - 3.35-1
- Update to 3.35

* Wed Apr 04 2012 Parag Nemade <pnemade AT redhat DOT com> - 3.34-1
- Update to 3.34

* Wed Mar 14 2012 Parag Nemade <pnemade AT redhat DOT com> - 3.33-1
- Update to 3.33

* Thu Feb 09 2012 Parag Nemade <pnemade AT redhat DOT com> - 3.32.2-1
- Update to 3.32.2

* Sat Feb 04 2012 Parag Nemade <pnemade AT redhat DOT com> - 3.32.1-1
- Update to 3.32.1

* Thu Jan 12 2012 Parag Nemade <pnemade AT redhat DOT com> - 3.32-1
- Update to 3.32

* Mon Dec 05 2011 Parag Nemade <pnemade AT redhat DOT com> - 3.31-1
- Update to 3.31

* Mon Nov 07 2011 Parag Nemade <pnemade AT redhat DOT com> - 3.30-1
- Update to 3.30

* Mon Oct 03 2011 Parag Nemade <pnemade AT redhat DOT com> - 3.29-1
- Update to 3.29

* Tue Sep 06 2011 Parag Nemade <pnemade AT redhat DOT com> - 3.28-1
- Update to 3.28

* Mon Aug 08 2011 Parag Nemade <pnemade AT redhat DOT com> - 3.27.1-1
- Update to 3.27.1

* Wed Jul 13 2011 Parag Nemade <pnemade AT redhat DOT com> - 3.27-1
- Update to 3.27

* Mon May 02 2011 Parag Nemade <pnemade AT redhat.com> - 3.25.1-1
- Update to 3.25.1

* Sun Apr  3 2011 Christopher Aillon <caillon@redhat.com> - 3.25-1
- Update to 3.25

* Mon Mar 07 2011 Parag Nemade <pnemade AT redhat.com> - 3.24.2-1
- Update to 3.24.2

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.24.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 09 2011 Parag Nemade <pnemade AT redhat.com> - 3.24.1-1
- Update to 3.24.1

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 07 2011 Parag Nemade <pnemade AT redhat.com> - 3.24-1
- Update to 3.24

* Mon Dec 06 2010 Parag Nemade <pnemade AT redhat.com> - 3.23-1
- Update to 3.23

* Tue Nov 09 2010 Parag Nemade <pnemade AT redhat.com> - 3.22-1
- Update to 3.22

* Mon Oct 04 2010 Parag Nemade <pnemade AT redhat.com> - 3.21-1
- Update to 3.21

* Tue Sep 07 2010 Parag Nemade <pnemade AT redhat.com> - 3.20-1
- Update to 3.20
- Drop buildroot, %%clean and cleaning buildroot in %%install

* Wed Aug 04 2010 Parag Nemade <pnemade AT redhat.com> - 3.19-1
- Update to 3.19

* Mon Jul 05 2010 Parag Nemade <pnemade AT redhat.com> - 3.18-1
- Update to 3.18

* Wed Jun 16 2010 Parag Nemade <pnemade AT redhat.com> - 3.17-1
- Update to 3.17

* Mon May 03 2010 Parag Nemade <pnemade AT redhat.com> - 3.16-1
- Update to 3.16

* Mon Apr 05 2010 Parag Nemade <pnemade AT redhat.com> - 3.15-1
- Update to 3.15

* Tue Mar 02 2010 Parag Nemade <pnemade AT redhat.com> - 3.14-1
- Update to 3.14

* Tue Feb 02 2010 Parag Nemade <pnemade AT redhat.com> - 3.13-1
- Update to 3.13

* Tue Jan 12 2010 Parag Nemade <pnemade AT redhat.com> - 3.12.1-1
- Update to 3.12.1

* Wed Dec 02 2009 Parag Nemade <pnemade AT redhat.com> - 3.12-1
- Update to 3.12

* Mon Nov 02 2009 Parag Nemade <pnemade@redhat.com> - 3.11.1-1
- Update to 3.11.1

* Fri Oct 23 2009 Parag Nemade <pnemade@redhat.com> - 3.11-1
- Update to 3.11

* Thu Sep 17 2009 Parag Nemade <pnemade@redhat.com> - 3.10.3-1
- Update to 3.10.3

* Wed Aug 05 2009 Parag Nemade <pnemade@redhat.com> - 3.10.2-1
- Update to 3.10.2

* Tue Aug 04 2009 Parag Nemade <pnemade@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 02 2009 Parag Nemade <pnemade@redhat.com> - 3.10-2
- Upstream stopped providing iso_639.tab file since 3.9 release,
  so remove it from %%files.

* Tue Jun 02 2009 Parag Nemade <pnemade@redhat.com> - 3.10-1
- Update to 3.10

* Mon Apr 27 2009 Christopher Aillon <caillon@redhat.com> - 3.8-1
- Update to 3.8

* Sun Mar 22 2009 Christopher Aillon <caillon@redhat.com> - 3.7-1
- Update to 3.7

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb  2 2009 Christopher Aillon <caillon@redhat.com> - 3.6-1
- Update to 3.6

* Mon Jan  5 2009 Christopher Aillon <caillon@redhat.com> - 3.5.1-1
- Update to 3.5.1

* Tue Dec  9 2008 Christopher Aillon <caillon@redhat.com> - 3.5-1
- Update to 3.5

* Sat Sep 20 2008 Ville Skyttä <ville.skytta at iki.fi> - 3.3-1
- Update to 3.3.
- Address minor issues in merge review (#225918): update %%description,
  don't use %%makeinstall, drop unneeded %%debug_package override, use
  parallel build.

* Wed Jul  2 2008 Christopher Aillon <caillon@redhat.com> - 3.1-1
- Update to 3.1

* Wed May  7 2008 Christopher Aillon <caillon@redhat.com> 2.1-1
- Update to 2.1

* Sun Mar  9 2008 Christopher Aillon <caillon@redhat.com> 2.0-1
- Update to 2.0

* Wed Feb 27 2008 Christopher Aillon <caillon@redhat.com> 1.9-1
- Update to 1.9

* Tue Feb  5 2008 Matthias Clasen <mclasen@redhat.com> 1.8-2
- Bump gettext BR
- Use the smaller .bz2 tarball

* Sat Feb  2 2008 Matthias Clasen <mclasen@redhat.com> 1.8-1
- Update to 1.8

* Sat Dec 29 2007 Christopher Aillon <caillon@redhat.com> 1.7-1
- Update to 1.7

* Tue Dec  4 2007 Christopher Aillon <caillon@redhat.com> 1.6-1
- Update to 1.6

* Fri Oct 26 2007 Christopher Aillon <caillon@redhat.com> 1.5-1
- Update to 1.5

* Wed Sep  5 2007 Christopher Aillon <caillon@redhat.com> 1.4-1
- Update to 1.4

* Wed Aug  8 2007 Matthias Clasen <mclasen@redhat.com> 1.3-1
- Update to 1.3
- Update the license field
- Use %%find_lang for translations
- Don't create debuginfo

* Tue Jul 24 2007 Parag Nemade  <pnemade@redhat.com> 
- Update to 1.2

* Wed Mar  7 2007 Christopher Aillon <caillon@redhat.com> 1.0-1
- Update to 1.0

* Fri Oct 20 2006 Christopher Aillon <caillon@redhat.com> 0.56-1
- Update to 0.56

* Mon Aug 28 2006 Christopher Aillon <caillon@redhat.com> 0.53-1
- Update to 0.53

* Sat Jun 24 2006 Jesse Keating <jkeating@redhat.com> 0.49-2
- Missing BR gettext

* Sun Jan  1 2006 Christopher Aillon <caillon@redhat.com> 0.49-1
- Update to 0.49

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Aug 26 2005 Christopher Aillon <caillon@redhat.com> 0.47-1
- Update to 0.47

* Mon Jun 13 2005 Christopher Aillon <caillon@redhat.com> 0.46-2
- The .pc file should be installed in %%{_datadir} instead of %%{_libdir}
  since this is a noarch package.  64bit platforms will otherwise look in
  the 64bit version of the %%{_libdir} and not find the .pc file and 
  cause them to not find iso-codes

* Fri Jun 10 2005 Christopher Aillon <caillon@redhat.com> 0.46-1
- Initial RPM
