Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           dumpet
Version:        2.1
Release:        21%{?dist}
Summary:        A tool to dump and debug bootable CD images
License:        GPLv2+
URL:            https://fedorahosted.org/dumpet/
BuildRequires:  gcc
BuildRequires:  popt-devel pkgconfig libxml2-devel git

Source0:        https://fedorahosted.org/releases/d/u/dumpet/dumpet-%{version}.tar.bz2
Patch0001: 0001-Manually-tell-it-we-ve-got-64-bit-files-because-32-b.patch

%description
DumpET is a utility to aid in the debugging of bootable CD-ROM images.

%prep
%setup -q
git init
git config user.email "%{name}-owner@fedoraproject.org"
git config user.name "Fedora Ninjas"
git add .
git commit -a -q -m "%{version} baseline."
git am %{patches} </dev/null

%build
make %{?_smp_mflags} CFLAGS="%{optflags} $(pkg-config --cflags libxml-2.0)"

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
make DESTDIR=%{buildroot} install

%files
%doc README TODO COPYING
%attr(644,root,root) %{_mandir}/man1/dumpet.1*
%{_bindir}/dumpet

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1-21
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 01 2014 Peter Jones <pjones@redhat.com> - 2.1-9
- Make sure 32-bit OSes can read 64-bit files.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 08 2010 Peter Jones <pjones@redhat.com> - 2.1-2
- Rebuild for new libxml2.

* Wed Aug 25 2010 Peter Jones <pjones@redhat.com> - 2.1-1
- Minor fixes (cjwatson)
- Add a man page (cjwatson)

* Fri Oct 16 2009 Peter Jones <pjones@redhat.com> - 2.0-1
- This is the 2.0 release.  It is awesome and adds XML output in order to
  support automated validation of CD images.

* Mon Oct 05 2009 Peter Jones <pjones@redhat.com> - 1.1-1
- Update to dumpet-1.1, which treats CFLAGS reasonably.

* Mon Oct 05 2009 Peter Jones <pjones@redhat.com> - 1.0-1
- First release.

