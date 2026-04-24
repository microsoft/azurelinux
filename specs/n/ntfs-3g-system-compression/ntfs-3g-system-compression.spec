# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:     ntfs-3g-system-compression
Summary:  NTFS-3G plugin for reading "system compressed" files
Version:  1.1
Release: 2%{?dist}
License:  GPL-2.0-or-later
URL:      https://github.com/ebiggers/ntfs-3g-system-compression
Source:   %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconfig(libntfs-3g) >= 2017.3.23
Supplements:    ntfs-3g

%description
System compression, also known as "Compact OS", is a Windows feature that
allows rarely modified files to be compressed using the XPRESS or LZX
compression formats. It is not built directly into NTFS but rather is
implemented using reparse points. This feature appeared in Windows 10 and it
appears that many Windows 10 systems have been using it by default.

This RPM contains a plugin which enables the NTFS-3G FUSE driver to
transparently read from system-compressed files. Currently, only reading is
supported. Compressing an existing file may be done by using the "compact"
utility on Windows.

%prep
%autosetup -p1

%conf
autoreconf -i
%configure

%build
%make_build

%install
%make_install
rm -rf %{buildroot}%{_libdir}/ntfs-3g/*.la

%files
%doc README.md
%license COPYING
%dir %{_libdir}/ntfs-3g/
%{_libdir}/ntfs-3g/ntfs-plugin-80000017.so

%changelog
* Mon Jan 05 2026 Neal Gompa <ngompa@fedoraproject.org> - 1.1-1
- Update to 1.1
- Slightly modernize spec
- Drop unneeded patch

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Mar 10 2023 DJ Delorie <dj@redhat.com> - 1.0-13
- Fix C99 compatibility issue

* Mon Feb 13 2023 Kamil Páral <kparal@redhat.com> - 1.0-12
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 08 2022 Richard W.M. Jones <rjones@redhat.com> - 1.0-9
- Rebuild for ntfs-3g CVE

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 31 2021 Richard W.M. Jones <rjones@redhat.com> - 1.0-7
- Rebuild for updated ntfs-3g CVE (RHBZ#1999788)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 26 2019 Kamil Páral <kparal@redhat.com> - 1.0-1
- initial package
