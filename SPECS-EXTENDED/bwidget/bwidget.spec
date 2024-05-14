Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitelib: %global tcl_sitelib %{_datadir}/tcl%{tcl_version}}

Name:           bwidget
Version:        1.9.7
Release:        15%{?dist}
Summary:        Extended widget set for Tk

License:        TCL
URL:            https://tcllib.sourceforge.net/
Source0:        https://downloads.sourceforge.net/tcllib/bwidget-%{version}.tar.gz

BuildArch:      noarch
Requires:       tcl(abi) = 8.6 tk
BuildRequires:  tcl

%description
An extended widget set for Tcl/Tk.

%prep
%setup -q
%{__sed} -i 's/\r//' LICENSE.txt

%build
# Nothing to build!

%install
# Don't bother with the included configure script and Makefile.  They
# are missing a lot of pieces and won't work at all.  Installation is
# pretty simple, so we can just do it here manually.
mkdir -p %{buildroot}/%{tcl_sitelib}/%{name}%{version}/
mkdir %{buildroot}/%{tcl_sitelib}/%{name}%{version}/lang
mkdir %{buildroot}/%{tcl_sitelib}/%{name}%{version}/images

install -m 0644 -pD *.tcl %{buildroot}/%{tcl_sitelib}/%{name}%{version}/
install -m 0644 -pD lang/*.rc %{buildroot}/%{tcl_sitelib}/%{name}%{version}/lang/
install -m 0644 -pD images/*.gif images/*.xbm %{buildroot}/%{tcl_sitelib}/%{name}%{version}/images/

%files
%{tcl_sitelib}/%{name}%{version}
%doc README.txt LICENSE.txt
%doc BWman/*.html

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.9.7-15
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.7-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.7-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1.9.7-4
- Changed requires to require tcl-8.6

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1.9.7-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Fri Feb 21 2014 Dmitrij S. Kryzhevich <krege@land.ru> - 1.9.7-2
- Fix filenames.

* Fri Feb 21 2014 Dmitrij S. Kryzhevich <krege@land.ru> - 1.9.7-1
- Update to new 1.9.7.
- Clean up spec file.
- Fix Fri Jan 3 2008 to Thu 3 2008.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 10 2010 Wart <wart@kobold.org> 1.9.0-1
- Update to 1.9.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan  3 2008 Marcela Maslanova <mmaslano@redhat.com> 1.8.0-3
- rebuild with new tcl8.5, changed abi in spec

* Wed Aug 22 2007 Wart <wart at kobold.org> 1.8.0-2
- License tag clarification
- Move files to a tcl-specific directory for faster loading

* Thu Oct 19 2006 Wart <wart at kobold.org> 1.8.0-1
- Update to 1.8.0
- Remove patch that was accepted upstream

* Mon Aug 28 2006 Wart <wart at kobold.org> 1.7.0-4
- Rebuild for Fedora Extras

* Fri Aug 11 2006 Wart <wart at kobold.org> 1.7.0-3
- Add patch for adding a color selector to the font dialog

* Sat Dec 10 2005 Wart <wart at kobold.org> 1.7.0-2
- added dist tag to release tag.

* Sat Dec 10 2005 Wart <wart at kobold.org> 1.7.0-1
- Initial spec file.
