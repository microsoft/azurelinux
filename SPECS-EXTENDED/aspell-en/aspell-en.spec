Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%define lang en
%define langrelease 0
%define aspellversion 6
Summary: English dictionaries for Aspell
Name: aspell-%{lang}
Version: 2019.10.06
Release: 4%{?dist}
License: MIT and BSD
URL: https://aspell.net/
Source: ftp://ftp.gnu.org/gnu/aspell/dict/%{lang}/aspell%{aspellversion}-%{lang}-%{version}-%{langrelease}.tar.bz2
Buildrequires: aspell >= 0.60
Requires: aspell >= 0.60
Obsoletes: aspell-en-gb <= 0.33.7.1
Obsoletes: aspell-en-ca <= 0.33.7.1

%define debug_package %{nil}

%description
Provides the word list/dictionaries for the following: English, Canadian
English, British English

%prep
%setup -q -n aspell%{aspellversion}-%{lang}-%{version}-%{langrelease}

%build
./configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%files
%doc Copyright
%{_libdir}/aspell-0.60/*

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 2019.10.06-4
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 50:2019.10.06-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 50:2019.10.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 08 2019 Nikola Forró <nforro@redhat.com> - 50:2019.10.06-1
- Update to version 2019.10.06
  resolves #1758940

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 50:2018.04.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 50:2018.04.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 50:2018.04.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 17 2018 Nikola Forró <nforro@redhat.com> - 50:2018.04.16-1
- Update to version 2018.04.16
  resolves #1568393

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 50:2017.08.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Aug 29 2017 Nikola Forró <nforro@redhat.com> - 50:2017.08.24-1
- Update to version 2017.08.24
  resolves #1485079

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 50:2015.04.24-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 50:2015.04.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 50:2015.04.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 50:2015.04.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 24 2015 Nikola Forró <nforro@redhat.com> - 50:2015.04.24-1
- Update to version 2015.04.24
  resolves #1284167

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 50:7.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 50:7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 50:7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 50:7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 50:7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 50:7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 50:7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 50:7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Ivana Hutarova Varekova <varekova@redhat.com> 50:7.1-1
- update to aspell6-en-7.1

* Mon Jan  3 2011 Ivana Hutarova Varekova <varekova@redhat.com> 50:7.0-1
- update to aspell6-en-7.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 50:6.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 50:6.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 50:6.0-9
- Autorebuild for GCC 4.3

* Thu Aug 30 2007 Ivana Varekova <varekova@redhat.com> - 50:6.0-8
- fix #62225 - add practice to gb world lists

* Fri Mar 30 2007 Ivana Varekova <varekova@redhat.com> - 50:6.0-7
- add version to obstolete flag

* Thu Mar 29 2007 Ivana Varekova <varekova@redhat.com> - 50:6.0-5
- add documentation
- change license tag

* Thu Mar 29 2007 Ivana Varekova <varekova@redhat.com> - 50:6.0-4
- update default buildroot

* Thu Mar 29 2007 Ivana Varekova <varekova@redhat.com> - 50:6.0-3
- update to aspell6
- use configure script to create Makefile
- some minor spec changes

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 50:6.0-2.1
- rebuild

* Fri Mar  3 2006 Ivana Varekova <varekova@redhat.com> - 50:6.0-2
- removed "offencive" (#154352), add "practice" (#62225)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 50:6.0-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 50:6.0-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Jul 18 2005 Ivana Varekova <varekova@redhat.com> 50:6.0-1
- update to aspell5-en-6.0
- build with aspell-0.60.3

* Mon Apr 11 2005 Ivana Varekova <varekova@redhat.com> 50:0.51-12
- rebuilt

* Wed Sep 29 2004 Adrian Havill <havill@redhat.com> 50:0.51-11
- remove debuginfo

* Thu Aug 26 2004 Adrian Havill <havill@redhat.com> 50:0.51-10
- obsolete -en-gb and -en-ca for upgrades

* Wed Aug 11 2004 Adrian Havill <havill@redhat.com> 50:0.51-9
- sync epoch with other aspell dicts, upgrade to 0.51-1

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun 23 2003 Adrian Havill <havill@redhat.com> 0.51-6
- data files are not arch independent

* Fri Jun 20 2003 Adrian Havill <havill@redhat.com> 0.51-5
- first build for new aspell (0.50)
