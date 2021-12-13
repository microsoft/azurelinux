Vendor:         Microsoft Corporation
Distribution:   Mariner
%global         _hardened_build 1

Summary:        Optimizer for PNG (Portable Network Graphics) files
Name:           pngcrush
Version:        1.8.13
Release:        7%{?dist}
License:        zlib
URL:            http://pmt.sourceforge.net/%{name}/
Source0:        http://downloads.sourceforge.net/pmt/%{name}-%{version}-nolib.tar.xz
# from Debian sid.
Source1:        %{name}.sgml
BuildRequires:  docbook-utils
BuildRequires:  gcc
BuildRequires:  libpng-devel
BuildRequires:  pkgconfig
BuildRequires:  zlib-devel

%description
pngcrush is a commandline optimizer for PNG (Portable Network Graphics) files.
Its main purpose is to reduce the size of the PNG IDAT datastream by trying
various compression levels and PNG filter methods. It also can be used to
remove unwanted ancillary chunks, or to add certain chunks including gAMA,
tRNS, iCCP, and textual chunks. 

%prep
%setup -q -n %{name}-%{version}-nolib
cp %{SOURCE1} . 

%build
rm -f z*.h crc32.h deflate.h inf*.h trees.h png*.h # force using system headers
pngflags=$(pkg-config --cflags --libs libpng)
gcc %{optflags} $pngflags -lz -o %{name} %{name}.c
docbook2man %{name}.sgml

%install
%{__install} -D -m0755 %{name} %{buildroot}%{_bindir}/%{name}
%{__install} -D -m0644 %{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

%files
%doc ChangeLog.html
%license LICENSE
%{_bindir}/%{name}
%doc %{_mandir}/man1/%{name}.1.gz

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.8.13-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 08 2018 Josef Ridky <jridky@redhat.com> - 1.8.13-2
- remove Group tag

* Tue Feb 20 2018 Nils Philippsen <nils@tiptoe.de> - 1.8.13-1
- version 1.8.13
- ship license
- remove some old packaging cruft
- require gcc for building

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Jan 21 2018 François Cami <fcami@fedoraproject.org> - 1.8.11-1
- New upstream release.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Mar 28 2016 François Cami <fcami@fedoraproject.org> - 1.8.0-1
- New upstream release.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.88-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 14 2015 François Cami <fcami@fedoraproject.org> - 1.7.88-1
- New upstream release.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.82-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 05 2015 François Cami <fcami@fedoraproject.org> - 1.7.82-1
- New upstream release.

* Mon Nov 24 2014 François Cami <fcami@fedoraproject.org> - 1.7.81-1
- New upstream release.

* Thu Oct 23 2014 François Cami <fcami@fedoraproject.org> - 1.7.78-1
- New upstream release.
- Add man page from Debian sid (1.7.65-0.1).

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.70-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.70-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Dec 29 2013 François Cami <fcami@fedoraproject.org> - 1.7.70-1
- New upstream release.

* Mon Dec 16 2013 François Cami <fcami@fedoraproject.org> - 1.7.69-2
- Fix changelog.

* Mon Dec 16 2013 François Cami <fcami@fedoraproject.org> - 1.7.69-1
- New upstream release.

* Tue Jul 30 2013 François Cami <fcami@fedoraproject.org> - 1.7.66-1
- New upstream release.

* Tue Jul 30 2013 François Cami <fcami@fedoraproject.org> - 1.7.59-3
- Fix obvious typos in description.

* Sun Jun  2 2013 François Cami <fcami@fedoraproject.org> - 1.7.59-2
- Switch to the smaller -nolib archive.

* Fri May 31 2013 François Cami <fcami@fedoraproject.org> - 1.7.59-1
- New upstream release.
- Use more macros.
- Switch to hardened build.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.43-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 13 2013 François Cami <fcami@fedoraproject.org> - 1.7.43-1
- New upstream release.

* Tue Jul 31 2012 Jon Ciesla <limburgher@gmail.com> - 1.7.35-1
- Update to latest to fix FTBFS.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.6.10-8
- Rebuild for new libpng

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 16 2010 Gerd Hoffmann <kraxel@redhat.com> - 1.6.10-6
- Fix FTBFS (#565047).

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 3 2008 - Gerd Hoffmann <kraxel@redhat.com> - 1.6.10-3.fc9
- remove all unneeded (zlib/libpng copy) header files.
- fix Source: URL.
- get cflags and libs from pkg-config.

* Fri Oct 31 2008 - Gerd Hoffmann <kraxel@redhat.com> - 1.6.10-2.fc9
- use $RPM_OPT_FLAGS.
- use systems zlib and libpng.

* Wed Oct 15 2008 - Gerd Hoffmann <kraxel@redhat.com> - 1.6.10-1.fc9
- update to 1.6.10.
- add dist tag to release.
- fix license.
- fix rpmlint warnings.

* Mon Jul 07 2008 - Patrick Steiner <patrick.steiner@a1.net> - 1.6.7-1
- Initial package.
