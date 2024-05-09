Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: pngnq
Summary: Pngnq is a tool for quantizing PNG images in RGBA format
Version: 1.1
Release: 23%{?dist}
License: BSD with advertising and MIT and BSD
URL: https://pngnq.sourceforge.net/
Source0: https://downloads.sourceforge.net/pngnq/pngnq-%{version}.tar.gz
Patch0: pngnq-libpng15.patch

BuildRequires: libpng-devel
BuildRequires: gcc

%description
Pngnq is a tool for quantizing PNG images in RGBA format.

The neuquant algorithm uses a neural network to optimise the color
map selection. This is fast and quite accurate, giving good results
on many types of images.

%prep
%autosetup -p1

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__make} DESTDIR=%{buildroot} install

%files
%doc COPYING README*
%{_bindir}/*
%{_mandir}/man1/*1*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1-23
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 04 2018 Josef Ridky <jridky@redhat.com> - 1.1-18
- Remove redundant defattr directive

* Thu Mar 08 2018 Josef Ridky <jridky@redhat.com> - 1.1-17
- Remove Group tag and add gcc dependency

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Nils Philippsen <nils@redhat.com> - 1.1-6
- update sourceforge download URL

* Wed Aug 01 2012 Jon Ciesla <limburgher@gmail.com> - 1.1-5
- Tom Lane's libpng15 fixes, BZ 843655.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.1-2
- Rebuild for new libpng

* Thu Jun 23 2011 - Gerd Hoffmann <kraxel@redhat.com> - 1.1-1
- Update to version 1.1 (#714728).

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 16 2010 - Gerd Hoffmann <kraxel@redhat.com> - 0.5-8
- Fix FTBFS by adding -lz -lm to ldlibs (#564721).

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 3 2008 - Gerd Hoffmann <kraxel@redhat.com> - 0.5-5.fc9
- add comments to the patches.
- fix rpm macro usage.

* Fri Oct 31 2008 - Gerd Hoffmann <kraxel@redhat.com> - 0.5-4.fc9
- Updated Licence tag, according to advice from fedora-legal.

* Fri Oct 31 2008 - Gerd Hoffmann <kraxel@redhat.com> - 0.5-3.fc9
- Use $RPM_OPT_FLAGS.
- Also package up pngcomp.

* Wed Oct 15 2008 - Gerd Hoffmann <kraxel@redhat.com> - 0.5-2.fc9
- add dist tag to release.
- fix rpmlint warnings.
- TODO: licence to be clarified.

* Mon Jul 26 2008 - Patrick Steiner <patrick.steiner@a1.net> - 0.5-1
- Initial package.
