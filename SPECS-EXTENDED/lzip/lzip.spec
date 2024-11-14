Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           lzip
Version:        1.25
Release:        2%{?dist}
Summary:        LZMA compressor with integrity checking

License:        GPL-2.0-or-later
URL:            http://www.nongnu.org/lzip/lzip.html
Source0:        https://download-mirror.savannah.gnu.org/releases/lzip/lzip-%{version}.tar.gz
Source1:        https://download-mirror.savannah.gnu.org/releases/lzip/lzip-%{version}.tar.gz.sig
BuildRequires: make
BuildRequires:  gcc-c++

%description
Lzip compresses data using LZMA (Lempel-Ziv-Markov chain-Algorithm). It
supports integrity checking using CRC (Cyclic Redundancy Check). To archive
multiple files, tar can be used with lzip. Please note, that the lzip file
format (.lz) is not compatible with the lzma file format (.lzma).

%prep
%setup -q
# file needs to be copied, because it is used in "make check"
cp -a COPYING{,.txt}
# convert CRLF to LF
sed -i 's/\r//' COPYING.txt 

%build
%configure CXXFLAGS="%{build_cxxflags}" LDFLAGS="%{build_ldflags}"
%make_build

%install
%make_install install-man

# if install-info is present, this is created by upstream's makefile
rm -Rf $RPM_BUILD_ROOT%{_infodir}/dir

%check
make check

%files
%license COPYING.txt
# TODO is currently empty
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/lzip
%{_infodir}/lzip.info*
%{_mandir}/man1/lzip.1*

%changelog
* Tue Apr 08 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 1.25-2
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License Verified

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Apr 09 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.24.1-2
- Correct license tag

* Mon Mar 04 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.24.1-1
- 1.24.1

* Tue Jan 30 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.24-1
- 1.24

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Mar 07 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.23-4
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Feb 03 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.23-1
- 1.23

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.22-1
- 1.22

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Sep  7 2019 Orion Poplawski <orion@nwra.com> - 1.21-1
- Update to 1.21

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Aug 01 2018 Gwyn Ciesla <limburgher@gmail.com> - 1.20-3
- BR Fix.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 14 2018 Gwyn Ciesla <limburgher@gmail.com> - 1.20-1
- 1.20

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 01 2017 Gwyn Ciesla <limburgher@gmail.com> - 1.19-1
- New upstream, 1446834.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jun 07 2016 Jon Ciesla <limburgher@gmail.com> - 1.18-1
- New upstream, 1342521.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jul 24 2015 Jon Ciesla <limburgher@gmail.com> - 1.17-1
- New upstream, 1246477.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.16-2
- Rebuilt for GCC 5 C++11 ABI change

* Wed Sep 10 2014 Jon Ciesla <limburgher@gmail.com> - 1.16-1
- New upstream, 1140119.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Oct 01 2013 Jon Ciesla <limburgher@gmail.com> - 1.15-1
- New upstream, 1014165.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 06 2013 Jon Ciesla <limburgher@gmail.com> - 1.14-1
- New upstream, 918416.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 13 2012 Jon Ciesla <limburgher@gmail.com> - 1.13-1
- New upstream, BZ 802973.
- lziprecover is now separate.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu May 05 2011 Jon Ciesla <limb@jcomserv.net> - 1.12-1
- Update to new release, BZ 702309.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 04 2010 Jon Ciesla <limb@jcomserv.net> - 1.11-1
- Update to new release, BZ 639555.

* Mon Jun 28 2010 Jon Ciesla <limb@jcomserv.net> - 1.10-1
- Update to new release, BZ 556767.

* Thu Dec 31 2009 Till Maas <opensource@till.name> - 1.8-1
- Update to new release
- Fix end of line encoding of COPYING

* Fri Aug 07 2009 Till Maas <opensource@till.name> - 1.7-2
- Exclude lzdiff & lzgrep, they will become part of zutils:
  http://www.nongnu.org/lzip/zutils.html
  and fixes a conflict with xz-lzma-compat: Red Hat Bugzilla #515502
- Use globbing for all manpages

* Tue Jul 28 2009 Till Maas <opensource@till.name> - 1.7-1
- Update to latest stable upstream
- remove upstreamed patch

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 15 2009 Till Maas <opensource@till.name> - 1.4-1
- Update to new release
- Add compile fixes for gcc 4.4 (missing #include <cstdio.h>)

* Thu Nov 27 2008 Till Maas <opensource@till.name> - 1.1-2
- fix type in summary
- call testsuite in %%check
- remove empty TODO file from %%doc

* Wed Nov 26 2008 Till Maas <opensource@till.name> - 1.1-1
- Initial spec for Fedora

