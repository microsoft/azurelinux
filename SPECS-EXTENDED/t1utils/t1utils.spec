Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary:        Collection of Type 1 and 2 font manipulation utilities
Name:           t1utils
Version:        1.42
Release:        2%{?dist}
# The Click license is an MIT variant.
License:        MIT
URL:            https://www.lcdf.org/~eddietwo/type/
Source0:        https://www.lcdf.org/~eddietwo/type/t1utils-%{version}.tar.gz
BuildRequires:  gcc

%description
t1utils is a collection of programs for manipulating PostScript type 1
and type 2 fonts containing programs to convert between PFA (ASCII)
format, PFB (binary) format, a human-readable and editable ASCII format,
and Macintosh resource forks.

%prep
%setup -q

%build
%configure
%make_build

%install
%make_install

%files
%license LICENSE
%doc NEWS.md README.md
%{_bindir}/t1ascii
%{_bindir}/t1asm
%{_bindir}/t1binary
%{_bindir}/t1disasm
%{_bindir}/t1mac
%{_bindir}/t1unmac
%{_mandir}/man1/t1ascii.1*
%{_mandir}/man1/t1asm.1*
%{_mandir}/man1/t1binary.1*
%{_mandir}/man1/t1disasm.1*
%{_mandir}/man1/t1mac.1*
%{_mandir}/man1/t1unmac.1*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.42-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Wed Dec 16 2020 Robert Scheck <robert@fedoraproject.org> 1.42-1
- Upgrade to 1.42

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.41-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Feb 14 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.41-3
- Patch for segfault in t1asm.

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Oct 26 2019 Robert Scheck <robert@fedoraproject.org> 1.41-1
- Update to 1.41

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.39-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.39-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.39-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.39-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.39-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.39-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.39-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.39-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 04 2015 Robert Scheck <robert@fedoraproject.org> 1.39-1
- Update to 1.39 (#1218365)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 08 2011 Robert Scheck <robert@fedoraproject.org> 1.37-1
- Update to 1.37

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Robert Scheck <robert@fedoraproject.org> 1.36-1
- Update to 1.36

* Thu Jul 30 2009 José Matos <jamatos@fc.up.pt> - 1.34-1
- New upstream release and fix issue with stricter gcc.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Sep  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.33-1
- fix license tag
- update to 1.33

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.32-10
- Autorebuild for GCC 4.3

* Tue Aug 28 2007 José Matos <jamatos[AT]fc.up.pt> - 1.32-9
- License fix, rebuild for devel (F8).

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 1.32-8
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 José Matos <jamatos[AT]fc.up.pt> - 1.32-7
- Rebuild for FC-6.

* Tue Feb 14 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 1.32-6
- Rebuild for Fedora Extras 5

* Tue Jan 17 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 1.32-5
- rebuild

* Mon Jan 16 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 1.32-4
- add %%{?dist} tag
- correct License

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.32-3
- rebuild on all arches

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Tue May 11 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:1.32-0.fdr.1
- Updated to 1.32.

* Wed Oct 22 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:1.29-0.fdr.1
- Updated to 1.29.

* Sat Aug 30 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:1.28-0.fdr.1
- Initial Fedora RPM release.
