Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           advancecomp
Version:        2.1
Release:        14%{?dist}
Summary:        Recompression utilities for png, mng, zip and gz files
License:        GPLv3
URL:            http://www.advancemame.it/
Source0:        https://github.com/amadvance/advancecomp/releases/download/v%{version}/advancecomp-%{version}.tar.gz

#  CVE-2019-8383 advancecomp: denial of service in function adv_png_unfilter_8
Patch0:         advancecomp-CVE-2019-8383.patch
# CVE-2019-9210 advancecomp: integer overflow in png_compress in pngex.cc
Patch1:         advancecomp-CVE-2019-9210.patch

BuildRequires:  gcc gcc-c++
BuildRequires:  tofrodos
BuildRequires:  zlib-devel
BuildRequires:  dos2unix

%description
AdvanceCOMP is a set of recompression utilities for .PNG, .MNG and .ZIP files.
The main features are :
* Recompress ZIP, PNG and MNG files using the Deflate 7-Zip implementation.
* Recompress MNG files using Delta and Move optimization.

This package contains:
* advzip - Recompression and test utility for zip files
* advpng - Recompression utility for png files
* advmng - Recompression utility for mng files
* advdef - Recompression utility for deflate streams in png, mng and gz files

%prep
%setup -q
%patch0 -p1 -b .CVE-2019-8383
%patch1 -p1 -b .CVE-2019-9210

dos2unix -k doc/*.txt

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files
%license COPYING
%doc AUTHORS HISTORY README
%doc doc/{adv*,authors,history,readme}.txt
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1-14
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 10 2019 Than Ngo <than@redhat.com> - 2.1-11
- Backport for #1708563, CVE-2019-8383 - denial of service in function adv_png_unfilter_8

* Wed Mar 06 2019 Than Ngo <than@redhat.com> - 2.1-10
- Backport, fix a buffer overflow with image of invalid size

* Fri Mar 01 2019 Than Ngo <than@redhat.com> - 2.1-9
- fixed CVE-2019-9210 advancecomp: integer overflow in png_compress in pngex.cc

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Matthias Saou <matthias@saou.eu> 2.1-7
- Fix doc EOL.
- Minor cosmetic updates (summary, description...).

* Sat Jul 14 2018 Christian Dersch <lupinix@fedoraproject.org> - 2.1-6
- BuildRequires: gcc-c++

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Than Ngo <than@redhat.com> - 2.1-4
- updated to 2.1 (fix CVE-2018-1056)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 28 2017 Christian Dersch <lupinix@mailbox.org> - 1.23-1
- new version

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Nov 13 2016 Christian Dersch <lupinix@mailbox.org> - 1.20-3
- revert to 1.20, 1.22 does not build and also needs unbundling of libdeflate first

* Sun Nov 13 2016 Christian Dersch <lupinix@mailbox.org> - 1.22-1
- new version

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 05 2015 Christian Dersch <lupinix@fedoraproject.org> - 1.20-1
- new version 1.20
- use license tag

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.19-4
- Rebuilt for GCC 5 C++11 ABI change

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 20 2014 Christopher Meng <rpm@cicku.me> - 1.19-1
- Update to 1.19

* Mon Feb 10 2014 Christopher Meng <rpm@cicku.me> - 1.18-1
- Update to 1.18

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 27 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.15-16
- Add disttag, modernise spec file

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-15
- Rebuilt for c++ ABI breakage

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.15-10
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Matthias Saou <http://freshrpms.net/> 1.15-9
- Rebuild for new BuildID feature.

* Fri Aug  3 2007 Matthias Saou <http://freshrpms.net/> 1.15-8
- Update License field.
- Remove dist tag, since the package will seldom change.

* Thu Mar 29 2007 Matthias Saou <http://freshrpms.net/> 1.15-7
- Switch to using DESTDIR install method.

* Thu Mar 29 2007 Matthias Saou <http://freshrpms.net/> 1.15-6
- Switch to use downloads.sf.net source URL.
- Tweak defattr.

* Mon Aug 28 2006 Matthias Saou <http://freshrpms.net/> 1.15-5
- FC6 rebuild, remove gcc-c++ build requirement (it's a default).

* Mon Mar  6 2006 Matthias Saou <http://freshrpms.net/> 1.15-4
- FC5 rebuild.

* Wed Feb  8 2006 Matthias Saou <http://freshrpms.net/> 1.15-3
- Rebuild for new gcc/glibc.

* Tue Jan 24 2006 Matthias Saou <http://freshrpms.net/> 1.15-2
- Rebuild for FC5.

* Wed Nov  2 2005 Matthias Saou <http://freshrpms.net/> 1.15-1
- Update to 1.15, includes 64bit fixes.

* Fri May 27 2005 Matthias Saou <http://freshrpms.net/> 1.14-5
- Update 64bit patch to a cleaner approach as Ralf suggested.

* Thu May 26 2005 Jeremy Katz <katzj@redhat.com> - 1.14-4
- fix build on 64bit arches

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.14-3
- rebuild on all arches

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 1.14-2
- rebuilt

* Wed Feb 23 2005 Matthias Saou <http://freshrpms.net/> 1.14-1
- Update to 1.14.

* Mon Nov 29 2004 Matthias Saou <http://freshrpms.net/> 1.13-1
- Update to 1.13.

* Tue Nov  2 2004 Matthias Saou <http://freshrpms.net/> 1.12-1
- Update to 1.12.

* Tue Aug 24 2004 Matthias Saou <http://freshrpms.net/> 1.11-1
- Update to 1.11.

* Mon May 17 2004 Matthias Saou <http://freshrpms.net/> 1.10-1
- Update to 1.10.

* Mon Nov  3 2003 Matthias Saou <http://freshrpms.net/> 1.7-2
- Rebuild for Fedora Core 1.
- Added missing build dependencies, thanks to mach.

* Tue Aug 26 2003 Matthias Saou <http://freshrpms.net/>
- Update to 1.7.

* Thu May 22 2003 Matthias Saou <http://freshrpms.net/>
- Initial RPM release.
